"""
Vlog Creator - LangGraph Project
==================================

Three agents working together as nodes in a LangGraph graph:

1. Research Agent
   - Takes a topic from the user
   - Searches the internet using SerpAPI (Google Search results)
   - Falls back to GPT knowledge if SerpAPI is unavailable

2. Vlog Writer Agent
   - Takes the topic + research findings
   - Uses GPT-4o-mini to write a complete, ready-to-record vlog script

3. SEO Optimizer Agent  ← NEW
   - Takes the vlog script + topic
   - Generates: YouTube title, description, tags, and thumbnail idea
str
Graph flow:
    START -> research_agent -> vlog_writer_agent -> seo_agent -> END
"""

import os
from typing import TypedDict, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper

load_dotenv()


# ---------------------------------------------------------------------------
# 1. Shared State
# ---------------------------------------------------------------------------
class VlogState(TypedDict):
    topic: str
    search_results: List[dict]
    research_summary: str
    vlog_script: str
    seo_output: str            # NEW: title, description, tags, thumbnail idea


# ---------------------------------------------------------------------------
# 2. Agent 1: Research Agent
# ---------------------------------------------------------------------------
def research_agent(state: VlogState) -> VlogState:
    print(f"\n[Research Agent] Searching the web for: '{state['topic']}'...")

    serpapi_key = os.getenv("SERPAPI_API_KEY") or os.getenv("SERP_API_KEY")
    if not serpapi_key:
        print("WARNING: No SerpAPI key. Using GPT fallback.")
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        response = llm.invoke(f"""
        You are a research assistant. Research this topic: {state['topic']}
        Provide: 
        1. Brief overview  
        2. 5 important facts  
        3. Latest trends  
        4. Interesting insights
        Format clearly.
        """)
        return {
            **state,
            "search_results": [],
            "research_summary": response.content,
        }

    try:
        search = SerpAPIWrapper(serpapi_api_key=serpapi_key)
        raw_results = search.results(state["topic"])
    except Exception as exc:
        print(f"WARNING: SerpAPI failed: {exc}")
        raw_results = {}

    organic_results = raw_results.get("organic_results", [])[:5]

    if not organic_results:
        print("WARNING: No results. Using GPT fallback.")
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        response = llm.invoke(f"Research this topic and give key facts and trends: {state['topic']}")
        return {
            **state,
            "search_results": [],
            "research_summary": response.content,
        }

    cleaned_results = []
    summary_lines = []
    for item in organic_results:
        title   = item.get("title", "")
        snippet = item.get("snippet", "")
        link    = item.get("link", "")
        cleaned_results.append({"title": title, "snippet": snippet, "link": link})
        summary_lines.append(f"- {title}: {snippet} ({link})")

    print(f"[Research Agent] Found {len(cleaned_results)} results.")
    return {
        **state,
        "search_results": cleaned_results,
        "research_summary": "\n".join(summary_lines),
    }


# ---------------------------------------------------------------------------
# 3. Agent 2: Vlog Writer Agent
# ---------------------------------------------------------------------------
def vlog_writer_agent(state: VlogState) -> VlogState:
    print("\n[Vlog Writer Agent] Drafting the vlog script...")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    prompt = f"""You are a professional vlog scriptwriter.

Topic: {state['topic']}

Research:
{state['research_summary']}

Write an engaging vlog script with:
1. Hook (first 5-10 seconds, grabs attention)
2. Intro (introduce the topic and what the viewer will learn)
3. Main content (3-5 key points based on the research)
4. Outro (summary + call to action: like/subscribe/comment)

Tone: conversational and energetic, speaking directly to camera.
Include stage directions in [brackets] where helpful.
"""
    response = llm.invoke(prompt)
    return {
        **state, 
        "vlog_script": response.content
        }


# ---------------------------------------------------------------------------
# 4. Agent 3: SEO Optimizer Agent  ← NEW
# ---------------------------------------------------------------------------
def seo_agent(state: VlogState) -> VlogState:
    print("\n[SEO Agent] Generating SEO package...")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

    prompt = f"""You are a YouTube SEO expert.

Topic: {state['topic']}

Here is the vlog script:
{state['vlog_script']}

Generate a complete YouTube SEO package with exactly this format:

TITLE:
(Write 3 YouTube title options, each under 70 characters, with keywords and curiosity)

DESCRIPTION:
(Write a 150-word YouTube description with keywords, what viewers will learn, and a call to action)

TAGS:
(List 15 comma-separated tags relevant to this topic)

THUMBNAIL IDEA:
(Describe in 2-3 sentences what the thumbnail should look like — colors, text overlay, image)
"""
    response = llm.invoke(prompt)
    return {
        **state, 
        "seo_output": response.content}


# ---------------------------------------------------------------------------
# 5. Build the Graph
# ---------------------------------------------------------------------------
def build_graph():
    graph = StateGraph(VlogState)

    graph.add_node("research_agent",   research_agent)
    graph.add_node("vlog_writer_agent", vlog_writer_agent)
    graph.add_node("seo_agent",        seo_agent)

    graph.add_edge(START,              "research_agent")
    graph.add_edge("research_agent",   "vlog_writer_agent")
    graph.add_edge("vlog_writer_agent", "seo_agent")
    graph.add_edge("seo_agent",        END)

    return graph.compile()


# ---------------------------------------------------------------------------
# 6. Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY is not set.")

    topic = input("Enter your vlog topic: ").strip()
    app   = build_graph()

    final_state = app.invoke({
        "topic": topic,
        "search_results": [],
        "research_summary": "",
        "vlog_script": "",
        "seo_output": "",
    })

    print("\n" + "=" * 60)
    print("RESEARCH SUMMARY")
    print("=" * 60)
    print(final_state["research_summary"])

    print("\n" + "=" * 60)
    print("FINAL VLOG SCRIPT")
    print("=" * 60)
    print(final_state["vlog_script"])

    print("\n" + "=" * 60)
    print("SEO PACKAGE")
    print("=" * 60)
    print(final_state["seo_output"])