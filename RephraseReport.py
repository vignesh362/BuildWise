import http.server
import socketserver
import webbrowser
import os
import socket

# Define the directory where your HTML, CSS, and JS files are located
web_dir = "/Users/vigneshshanmugasundaram/Code/htmlReport"  # Update with the correct path
os.chdir(web_dir)  # Set the working directory


def find_free_port():
    """Find an available port to start the server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def add_sections():
    """Function to dynamically add sections to the index.html file."""
    # Read the original HTML content
    with open("index.html", "r") as file:
        html_content = file.read()

    # Find the container markers
    sections_start_marker = '<div id="sections-container" class="sections-container">'
    sections_end_marker = '</div>'  # Closing tag of the sections container

    sidebar_start_marker = '<ul id="sidebar-list" class="sidebar-list">'
    sidebar_end_marker = '</ul>'  # Closing tag of the sidebar list

    # Check if the containers exist
    if sections_start_marker not in html_content or sidebar_start_marker not in html_content:
        print("Error: Placeholder not found in index.html")
        return

    # Locate the indices for the sections container
    sections_start_index = html_content.find(sections_start_marker) + len(sections_start_marker)
    sections_end_index = html_content.find(sections_end_marker, sections_start_index)

    # Locate the indices for the sidebar list
    sidebar_start_index = html_content.find(sidebar_start_marker) + len(sidebar_start_marker)
    sidebar_end_index = html_content.find(sidebar_end_marker, sidebar_start_index)

    # Collect new sections content and sidebar entries
    new_sections = ""
    new_sidebar_entries = ""

    print("Enter sections to add to the webpage (type 'done' to finish):\n")
    while True:
        section_type = input("Enter section type (text/image) or 'done': ").strip().lower()
        if section_type == "done":
            break

        heading = input("Enter heading: ").strip()
        if section_type == "text":
            content = input("Enter content: ").strip()
            new_sections += f"""
                <div class="section">
                    <h2>{heading}</h2>
                    <p>{content}</p>
                    <button class="delete-btn" onclick="deleteSection(this)">🗑️</button>
                </div>
            """
        elif section_type == "image":
            image_url = input("Enter image URL: ").strip()
            new_sections += f"""
                <div class="section">
                    <h2>{heading}</h2>
                    <img src="{image_url}" alt="{heading}" style="max-width: 100%; border-radius: 8px;">
                    <button class="delete-btn" onclick="deleteSection(this)">🗑️</button>
                </div>
            """
        else:
            print("Invalid section type. Please enter 'text' or 'image'.")

        # Add a new entry to the sidebar
        new_sidebar_entries += f"""
            <li onclick="scrollToSection('{heading}')">{heading}</li>
        """

    # Replace the container content with the new sections and sidebar entries
    updated_html = (
            html_content[:sections_start_index]  # Content before the sections container
            + new_sections  # New sections
            + html_content[sections_end_index:sidebar_start_index]  # Content between sections and sidebar
            + new_sidebar_entries  # New sidebar entries
            + html_content[sidebar_end_index:]  # Content after the sidebar container
    )

    # Write back the updated HTML
    with open("index.html", "w") as file:
        file.write(updated_html)
    print("Updated HTML content has been written and old content overridden.")

def start_server():
    """Function to start the server and open the webpage."""
    PORT = find_free_port()  # Find an available port

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        webbrowser.open(f"http://localhost:{PORT}/index.html")  # Open the page in the default browser
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")
            httpd.shutdown()


# Main script
if __name__ == "__main__":
    # Step 1: Update the HTML content
    add_sections()

    # Step 2: Start the server
    start_server()