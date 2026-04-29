from ddgs import DDGS

def web_search(query, max_results=5):
    results_data = []

    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)

            for r in results:
                results_data.append({
                    "title": r.get("title"),
                    "snippet": r.get("body"),
                    "link": r.get("href")
                })

    except Exception as e:
        return f"Web search failed: {str(e)}"

    return results_data