import requests
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from io import BytesIO

# Function to fetch movie details from TMDb
def fetch_movie_details_tmdb(title):
    api_key = "0a7a42d3e393653ba495817fab7e4201"  # Replace with your TMDb API key
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}"

    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        if data["results"]:
            movie = data["results"][0]
            movie_id = movie["id"]
            poster_path = movie.get("poster_path", None)
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits"
            details_response = requests.get(details_url)
            details_response.raise_for_status()
            details_data = details_response.json()

            movie_details = {
                "title": details_data.get("title", "N/A"),
                "imdb_rating": details_data.get("vote_average", "N/A"),
                "storyline": details_data.get("overview", "N/A"),
                "cast": ", ".join([cast["name"] for cast in details_data.get("credits", {}).get("cast", [])[:5]]),
                "poster_url": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
            }
            return movie_details
        else:
            return {"error": "Movie not found."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}

def search_movie(movie_title):
    details_label.config(state="normal")
    details_label.delete("1.0", tk.END)
    details_label.config(state="disabled")
    poster_label.config(image="")

    if not movie_title:
        messagebox.showwarning("Input Error", "Please enter a movie title.")
        return

    movie_details = fetch_movie_details_tmdb(movie_title)

    if "error" in movie_details:
        messagebox.showerror("Error", movie_details["error"])
    else:
        # Display movie details
        details_label.config(state="normal")
        details_label.insert(tk.END, f"Title: {movie_details['title']}\n")
        details_label.insert(tk.END, f"IMDb Rating: {movie_details['imdb_rating']}\n\n")
        details_label.insert(tk.END, f"Storyline: {movie_details['storyline']}\n\n")
        details_label.insert(tk.END, f"Cast: {movie_details['cast']}")
        details_label.config(state="disabled")

        # Display movie poster
        if movie_details["poster_url"]:
            response = requests.get(movie_details["poster_url"])
            poster_image = Image.open(BytesIO(response.content))
            poster_image = poster_image.resize((200, 300), Image.LANCZOS)

            poster = ImageTk.PhotoImage(poster_image)
            poster_label.config(image=poster)
            poster_label.image = poster

# Tkinter UI setup
root = tk.Tk()
root.title("Movie Database Management System")
root.geometry("600x500")
root.configure(bg="#f5f5f5")

# Title Label
title_label = tk.Label(root, text="Movie Database Management System", font=("Arial", 16, "bold"), bg="#f5f5f5", fg="#333")
title_label.pack(pady=10)

# Search Frame
search_frame = tk.Frame(root, bg="#f5f5f5")
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search Movie:", font=("Arial", 12), bg="#f5f5f5").grid(row=0, column=0, padx=5)
search_var = tk.StringVar()
tk.Entry(search_frame, textvariable=search_var, font=("Arial", 12), width=30).grid(row=0, column=1, padx=5)
tk.Button(search_frame, text="Search", font=("Arial", 12), command=lambda: search_movie(search_var.get())).grid(row=0, column=2, padx=5)

# Poster and Details Frame
content_frame = tk.Frame(root, bg="#f5f5f5")
content_frame.pack(pady=10, fill="both", expand=True)

poster_label = tk.Label(content_frame, bg="#f5f5f5")
poster_label.grid(row=0, column=0, padx=10)

details_label = tk.Text(content_frame, font=("Arial", 12), wrap="word", height=15, width=50, state="disabled", bg="#fff", fg="#333")
details_label.grid(row=0, column=1, padx=10)

# Run the application
root.mainloop()
