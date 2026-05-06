from collections import deque
import csv
import sys
import copy
from util import Node, StackFrontier, QueueFrontier


# Maps names to a set of corresponding person_ids
# Dictionary "tom hanks": {"nm0000158", "nm1234567"} (to handle duplicate names).
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
# Structure: {person_id: {"name": str, "birth": str, "movies": set()}}
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    data equals people, movies, stars
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:  # Opens file
        # Creating iterator + csv.DictReader(f) creates an ordered dictionary
        reader = csv.DictReader(f)
        # Each row is a dictionary representing one line (with keys: "id", "name", "birth") from people CSV
        for row in reader:
            people[row["id"]] = {   # row["id"] calls person_id, people[person_id] gets the dictionary (name, birth, movies)
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            # Populates names
            # row["names"] gets the name in row & if not in name map name to person_id
            if row["name"].lower() not in names:
                # {row["id"]} creates a set with person_id from current row in csv
                names[row["name"].lower()] = {row["id"]}
            else:
                # if name already in names, just add the person_id to the set (duplicate names)
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:  # Opens the movies CSV and decodes it using utf-8
        # Creates an iterator that returns each row as an OrderedDict
        reader = csv.DictReader(f)  # First row of CSV becomes the dictionary keys (id, title, year)
        # Row represents the current CSV row as a dictionary: row = {,,,}
        for row in reader:
            movies[row["id"]] = {   # Row["id"] is id for movie
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        """
        Try to add movie to the current set

        row["person_id"] gets person's ID from CSV row
        people[row["person_id"]] gets dictionary using iD + returns their data record
        ["movies"] accesses the movie set in people
        .add(row["movie_id"]) adds the movie ID from the current CSV row to the set of movies
        This actor attended this movie
        """
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:  # Acessing a non-existence dictionary key
                pass          # Silently ignore the error


def main():
    if len(sys.argv) > 2:  # sys.argv is the input used to run the code, separated by space as a list
        sys.exit("Usage: python degrees.py [directory]")
    # Uses the speficied folder, otherwise defaults to large
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # Ask for person ID
    source = person_id_for_name(input("Name: "))  # Ask for name, converts to ID
    if source is None:                            # ID is not found
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))  # Ask for target name, converts to ID
    if target is None:                            # Target is not found
        sys.exit("Person not found.")

    # Calculates the shortest link between the two actors (through shared movies)
    path = shortest_path(source, target)

    # Print connections
    if path is None:  # no connection exists
        print("Not connected.")
    else:
        # 1 degree: Two actors in the same movie together.
        degrees = len(path)
        print(f"{degrees} degrees of separation.")  # Prints how many steps apart
        # Prepares the path by adding the starting actor at position 0 (with no connecting movie)
        path = [(None, source)] + path
        for i in range(degrees):                      # Degrees is always 1 less than path length
            person1 = people[path[i][1]]["name"]      # Actor 1's name (movie_id, person_id) prev
            person2 = people[path[i + 1][1]]["name"]  # Actor 2's name
            movie = movies[path[i + 1][0]]["title"]   # Movie name connecting actor 1 and actor 2
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # source is person_id

    if source == target:
        return []  # Path of length 0

    queue = deque()
    queue.append([(None, source)])
    visited = set()

    while queue:
        lst = queue.popleft()
        now = lst[-1]
        if now[1] in visited:
            continue
        visited.add(now[1])
        if now[1] == target:
            return lst[1:]

        for movie_id, neighbor in neighbors_for_person(now[1]):
            if neighbor not in visited:
                lst1 = lst + [(movie_id, neighbor)]
                queue.append(lst1)

    return None


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,son
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set(
    )))  # Converts set of person_id of name, or an empty set if name not found, into a list
    if len(person_ids) == 0:                           # No name
        return None
    elif len(person_ids) > 1:                          # Duplicate names
        print(f"Which '{name}'?")                      # Ask for clarification
        for person_id in person_ids:
            person = people[person_id]                 # returns set from people[person_id]
            name = person["name"]                      # returns person's name
            birth = person["birth"]                    # returns person's birth date
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")  # Get user's input fr person
            if person_id in person_ids:                # if valid, return person_id
                return person_id
        except ValueError:                             # if not valid, ignore, return None
            pass
        return None
    else:                                              # One name
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]  # movies set that person_id has attended
    # Stores the movie_id and person_id pairs, person_id in neighbors are actors in movie woth person_id
    neighbors = set()
    for movie_id in movie_ids:               # Loops through each movie inside of movie_ids set
        # Accesses the neighboring actor within each movie
        for person_id in movies[movie_id]["stars"]:
            # Neighbors set adds the movie_id (moving connecting actor 1 to actor 2), actor 2
            neighbors.add((movie_id, person_id))
    return neighbors  # returns the set after all neighbors have been processed


if __name__ == "__main__":
    main()
