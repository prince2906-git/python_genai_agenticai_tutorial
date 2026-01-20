## Common GenAI Models and Tools
    Type : Text
    Model : GPT, BERT, Claude
    Tools/Libraries : Hugging Face, LangChain

    Type : Image
    Model : DALL-E, Stable Diffusion
    Tools/Libraries : Diffusers, Replicate

    Type : Audio
    Model : Bark, Jukebox
    Tools/Libraries : AudioKit, torchaudio, suno
    
    Type : Code
    Model : Codex, CodeLlama
    Tools/Libraries : OpenAI API, GitHub Copilot 

    Type : Video
    Model : Synthesia, Runway
    Tools/Libraries : VideoGen, FFmpeg


*** Most tools use Transformers architecture, and models are often trained on large datasets + unsupervised /fine-tuned learning.

## Transformer Architecture
    - **Key Components**:
        - **Self-Attention Mechanism**: Allows the model to weigh the importance of different words in a sentence.
        - **Positional Encoding**: Adds information about the position of words in a sequence.
        - **Multi-Head Attention**: Enables the model to focus on different parts of the input simultaneously.
        - **Feed-Forward Neural Networks**: Processes the output from the attention layers.
        - **Layer Normalization and Residual Connections**: Stabilizes training and improves performance.

    - **Training Process**:
        - Pre-training on large datasets using unsupervised learning.
        - Fine-tuning on specific tasks with labeled data.

    - **Advantages**:
        - Handles long-range dependencies effectively.
        - Scales well with large datasets and model sizes.

