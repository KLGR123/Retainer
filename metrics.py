import Levenshtein


def calculate_similarity(code1, code2):
    distance = Levenshtein.distance(code1, code2)
    similarity = 1 - (distance / max(len(code1), len(code2)))
    return similarity


if __name__ == "__main__":
    code_snippet_1 = "def add(a, b): return a + b"
    code_snippet_2 = "def add(x, y): return x + y"

    similarity_score = calculate_similarity(code_snippet_1, code_snippet_2)
    print(f"相似度: {similarity_score}")