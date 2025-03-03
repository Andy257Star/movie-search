from movie_search import MovieSearch

def wrap_text(text, width):
    """Переносит текст на новую строку по словам, не превышая указанную ширину."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 > width:  # +1 для пробела
            lines.append(current_line)
            current_line = word  # Начинаем новую строку
        else:
            current_line += (" " if current_line else "") + word  # Добавляем слово

    if current_line:
        lines.append(current_line)

    return "\n".join(lines)

def format_movie_output(movie):
    title, description, release_year, length, genre = movie[1], movie[2], movie[3], movie[4], movie[5]
    separator = "=" * 75  # Разделитель длиной 75 символов

    return (
        f"{separator}\n"
        f"Название фильма: \"{title}\"\n"
        f"Год выпуска: {release_year}\n"
        f"Длительность: {length} мин\n"
        f"Жанр: {genre}\n"
        f"Описание:\n{wrap_text(description, 75)}\n"
        f"{separator}"
    )

def main():
    search = MovieSearch()

    while True:
        command = input("Введите команду (search, genres, popular, exit): ").strip().lower()

        if command == "search":
            keywords = input("Введите ключевые слова для поиска: ").strip()
            results = search.search_by_keyword(keywords)
            if results:
                for film in results:
                    print(format_movie_output(film))
            else:
                print("Фильмы не найдены.")

        elif command == "genres":
            genres = search.get_available_genres()
            for i, genre in enumerate(genres, 1):
                print(f"{i}. {genre}")
            genre_input = input("Введите жанр (номер или название): ").strip()

            if genre_input.isdigit():
                genre_index = int(genre_input) - 1
                if 0 <= genre_index < len(genres):
                    genre = genres[genre_index]
                else:
                    print("Неверный номер жанра.")
                    continue
            else:
                genre = genre_input.capitalize()

            year = input("Введите год (опционально, нажмите Enter для пропуска): ").strip()
            if year.isdigit():
                results = search.search_by_genre_and_year(genre, int(year))
            else:
                results = search.search_by_genre(genre)

            if results:
                for film in results:
                    print(format_movie_output(film))
            else:
                print("Фильмы не найдены.")

        elif command == "popular":
            from logs import QueryLogger
            logger = QueryLogger()
            popular_queries = logger.get_popular_queries()
            if popular_queries:
                print("Популярные запросы:")
                for i, (query, count) in enumerate(popular_queries, 1):
                    print(f"{i}. {query} - {count} раз(а)")
            else:
                print("Популярных запросов пока нет.")

        elif command == "exit":
            print("Выход из программы.")
            break

        else:
            print("Неизвестная команда. Попробуйте снова.")

if __name__ == "__main__":
    main()
