# socialmedia.py

def get_social_prompt(platform, article_text):
    """
    Returns (prompt, temperature) for the specified social media platform.
    """
    if platform.lower() == "twitter":
        prompt = (
            "You are a professional copywriter. Write a single, engaging tweet based on the following article. "
            "Respond ONLY with the tweet itself, and nothing else. "
            "Your tweet must be in English and MUST NOT exceed 240 characters in total, including hashtags, emojis, and links. "
            "Strictly enforce this 240-character limit. Add emojis and 1–2 relevant hashtags. "
            "If the result is longer, rewrite and shorten it until it fits within 240 characters. "
            "Here is the article:\n\n"
            f"\"{article_text}\""
        )   
        temperature = 0.9
    elif platform.lower() == "linkedin":
        prompt = (
            "Please ignore all previous instructions. "
            "Please respond only in the English language. "
            "You are a LinkedIn content creator. "
            "Do not self reference. Do not explain what you are doing. "
            "Your content should be engaging, informative, and relevant for professionals across different industries. "
            "Include industry insights, personal experiences, and thought leadership while maintaining a genuine and conversational tone. "
            "Add emojis to the content when appropriate and write from a personal experience. "
            "The total content should be between 390 and 400 words, or a maximum of 2200 characters long and spaced out so it's easy for readers to scan through. "
            "Please add relevant hashtags to the post and encourage readers to comment.\n\n"
            f"Here is the article for reference:\n\"{article_text}\""
        )   
        temperature = 0.6
    elif platform.lower() == "facebook":
        prompt = (
            "Summarize the following article as a friendly, conversational Facebook post. "
            "Use a relaxed tone, maybe a question at the end, and one hashtag. "
            "Here's the article:\n\n"
            f"{article_text}"
        )
        temperature = 0.75
    else:
        # Default: simple summary
        prompt = f"Summarize the following article:\n\n{article_text}"
        temperature = 0.7

    return prompt, temperature


