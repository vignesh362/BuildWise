# streamlit_launcher.py
import subprocess
import os

def invoke_streamlit_app(text, image_path):
    """
    Invokes the Streamlit app with the given text and image path.
    """
    args_file = "streamlit_args.txt"
    with open(args_file, "w") as f:
        f.write(f"{text}\n")
        f.write(f"{image_path}\n")

    try:
        subprocess.run(
            ["streamlit", "run", "wordStreamlet.py", "--", args_file],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running Streamlit app: {e}")
    finally:
        if os.path.exists(args_file):
            os.remove(args_file)

if __name__ == "__main__":
    example_text = "This is a sample text to display in the Streamlit app."
    example_image_path = "/Users/vigneshshanmugasundaram/Documents/nyuLogo.png"
    invoke_streamlit_app(example_text, example_image_path)
