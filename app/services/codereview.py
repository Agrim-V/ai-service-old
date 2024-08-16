from github3 import login
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models.base import BaseChatModel
from langchain.chat_models import ChatOpenAI
from functools import lru_cache
from dotenv import load_dotenv
import os

load_dotenv('/Users/qoala/Desktop/services/ai-service/.env')

class GithubRetriever:
    def __init__(self, github_token, owner, repo_name, pr_number):
        self.gh = login(token=github_token)
        self.repo = self.gh.repository(owner, repo_name)
        self.pull_request = self.repo.pull_request(pr_number)

    def get_pr_details(self):
        files_changed = [file for file in self.pull_request.files()]
        commit_messages = [commit.message for commit in self.pull_request.commits()]
        pr_comments = [comment.body for comment in self.pull_request.issue_comments()]
        return {
            "description": self.pull_request.body,
            "files_changed": files_changed,
            "commit_messages": commit_messages,
            "pr_comments": pr_comments
        }
    
class PRSummaryChain:
    def __init__(self, code_summary_llm, pr_summary_llm):
        self.code_summary_llm = code_summary_llm
        self.pr_summary_llm = pr_summary_llm

    def run(self, pr_details):
        code_summaries = []
        for file in pr_details['files_changed']:
            summary = LLMChain(
                llm=self.code_summary_llm,
                prompt=PromptTemplate.from_template("Summarize the following code changes:\n{code_diff}")
            ).run(code_diff=file.patch)
            code_summaries.append(summary)
        
        pr_summary = LLMChain(
            llm=self.pr_summary_llm,
            prompt=PromptTemplate.from_template("Summarize this pull request:\n{description}")
        ).run(description=pr_details['description'])

        return {
            "pr_summary": pr_summary,
            "code_summaries": code_summaries
        }

class CodeReviewChain:
    def __init__(self, llm):
        self.llm = llm

    def run(self, pr_details):
        code_reviews = []
        for file in pr_details['files_changed']:
            review = LLMChain(
                llm=self.llm,
                prompt=PromptTemplate.from_template("Review the following code changes:\n{code_diff}")
            ).run(code_diff=file.patch)
            # Split the review into individual comments if necessary
            comments = [{"file_path": file.filename, "line_number": 1, "comment": review}]  # Example of one comment
            code_reviews.append({"file_path": file.filename, "review": review, "comments": comments})
        return {"code_reviews": code_reviews}
    
class PullRequestReporter:
    def __init__(self, pr_summary, code_summaries, pull_request, code_reviews):
        self.pr_summary = pr_summary
        self.code_summaries = code_summaries
        self.pull_request = pull_request
        self.code_reviews = code_reviews

    def report(self):
        report = f"### Pull Request Summary\n\n{self.pr_summary}\n\n"
        report += "### Code Summaries\n\n"
        for summary in self.code_summaries:
            report += f"{summary}\n\n"
        report += "### Code Reviews\n\n"
        for review in self.code_reviews:
            report += f"**File: {review['file_path']}**\n{review['review']}\n\n"
        return report

def perform_code_review(owner, repo, pr_number):
    github_token = os.getenv("GITHUB_TOKEN")
    retriever = GithubRetriever(github_token, owner, repo, pr_number)
    pr_details = retriever.get_pr_details()

    print(f"PR Details: {pr_details}.")

    # Initialize and run the summary chain
    pr_summary_chain = PRSummaryChain(
        code_summary_llm=load_gpt_llm(), 
        pr_summary_llm=load_gpt4_llm()
    )
    summary = pr_summary_chain.run(pr_details)

    # Initialize and run the code review chain
    code_review_chain = CodeReviewChain(llm=load_gpt_llm())
    reviews = code_review_chain.run(pr_details)

    # Generate the final report
    reporter = PullRequestReporter(
        pr_summary=summary["pr_summary"],
        code_summaries=summary["code_summaries"],
        pull_request=retriever.pull_request,
        code_reviews=reviews["code_reviews"]
    )
    # Optionally, post comments inline
    for review in reviews["code_reviews"]:
        for comment in review["comments"]:
            # Use the GitHub API to post the comment directly in the PR
            file_path = comment["file_path"]
            line_number = comment["line_number"]
            comment_text = comment["comment"]
            retriever.pull_request.create_review_comment(
                body=comment_text,
                commit_id=retriever.pull_request.head.sha,
                path=file_path,
                position=line_number
            )
    return reporter.report()

@lru_cache(maxsize=1)
def load_gpt_llm() -> BaseChatModel:
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo",
    )
    return llm

@lru_cache(maxsize=1)
def load_gpt4_llm():
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4",
    )
    return llm
