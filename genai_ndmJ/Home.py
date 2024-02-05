import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to NDM Gen-AI! 👋")


st.markdown(
    """
    Generative AI refers to a type of artificial intelligence system that is designed to generate content or data that is similar to what a human might create. This type of AI is often used in creative tasks, such as generating text, images, music, or even videos. It has the ability to produce content that is original and can sometimes be indistinguishable from what a human might create.

Generative AI systems are typically based on deep learning algorithms and neural networks. These algorithms are trained on large datasets of existing content, which allows them to learn patterns and relationships within the data. Once trained, the AI can generate new content by extrapolating from what it has learned.

Here are a few examples of how generative AI can be applied:

1. **Text Generation:** Generative AI can be used to generate human-like text, which has applications in content creation, chatbots, and even creative writing.

2. **Image Generation:** AI can generate images that resemble photographs or artwork. This is used in various creative applications, including the generation of artwork, graphic design, and even deepfake technology.

3. **Music Composition:** Generative AI can compose music that mimics the style of famous composers or create entirely new musical pieces.

4. **Video Generation:** It can also be used to generate videos, such as deepfake videos, or even assist in video editing and special effects.

5. **Data Augmentation:** In data science, generative AI can be used to create synthetic data to augment existing datasets for machine learning training.

Generative AI has made significant advancements in recent years, thanks to developments in deep learning, particularly using architectures like Generative Adversarial Networks (GANs) and Transformers. These technologies have opened up new possibilities in creativity, content generation, and automation across various industries, from entertainment and marketing to healthcare and finance. However, ethical considerations and potential misuse of generative AI have also become important topics of discussion.
"""
)