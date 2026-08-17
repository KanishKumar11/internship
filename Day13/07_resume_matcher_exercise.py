"""
07_resume_matcher_exercise.py - Your turn: build a resume matcher

TEACHES : Nothing new. Everything you need is in files 03, 04 and 05.
          This is where you type it yourself.
SLIDE   : Day 13, Slide 11 - Exercise, Resume Matcher (deck page 11/16)
RUN     : python 07_resume_matcher_exercise.py

THE BRIEF
    Compare a resume to a job description and report:
      1. a match score between 0.00 and 1.00
      2. the MISSING KEYWORDS - words the job description leans on that
         the resume never mentions

    That second part is the useful half. A score tells a candidate they
    scored 0.41; the missing keywords tell them what to write next.

HOW TO WORK
    The print statements are already here. Uncomment the TODO lines below
    them, fill in the blanks, and run the file after every single step -
    do not write all four lines and then hunt for the typo.

EXPECTED OUTPUT WHEN YOU ARE DONE
        Match score: 0.41
        Missing keywords: learning, machine, aws, deploy, learn, models,
                          scikit, services, train, wanted

    Stuck? File 08 is the full solution. Try for ten minutes first.

REQUIRES
    pip install scikit-learn
"""

# TODO: import TfidfVectorizer from sklearn.feature_extraction.text
# TODO: import cosine_similarity from sklearn.metrics.pairwise


RESUME = (
    "Python developer with two years of experience. I build REST APIs with "
    "Flask, write SQL queries, and analyse data with pandas. BCA graduate."
)

JOB_DESCRIPTION = (
    "Python developer wanted. Build REST APIs with Flask, write SQL queries, "
    "and analyse data with pandas. Train machine learning models with "
    "scikit-learn and deploy the machine learning services to AWS."
)

print("RESUME:")
print(f"   {RESUME}\n")
print("JOB DESCRIPTION:")
print(f"   {JOB_DESCRIPTION}\n")


# ----------------------------------------------------------------------
# PART 1 - the match score. Four lines, all of them from slide 8.
# ----------------------------------------------------------------------

# TODO: vectorizer = TfidfVectorizer(stop_words='english')
# TODO: vectors = vectorizer.fit_transform([RESUME, JOB_DESCRIPTION])
# TODO: match_score = cosine_similarity(vectors[0], vectors[1])[0][0]
# TODO: print(f"Match score: {match_score:.2f}")

# Watch out for these three, they catch everybody:
#   - fit_transform takes a LIST. The square brackets are not decoration.
#   - cosine_similarity returns a 2D array, so you need the [0][0] on the end.
#   - leave out stop_words='english' and "the", "a", "and" dominate the score.


# ----------------------------------------------------------------------
# PART 2 (BONUS) - the missing keywords
# ----------------------------------------------------------------------
# The plan, in English:
#   a. Ask the vectorizer for its vocabulary: vectorizer.get_feature_names_out()
#   b. Pull out the job description's row of TF-IDF weights. It is row 1
#      (the resume was row 0), and .toarray()[0] turns that sparse row into
#      a plain list of floats you can index.
#   c. Keep only the words the job actually leans on - weight > 0.1.
#   d. Of those, keep the ones that do NOT appear in the resume. Split the
#      resume with re.findall(r"[a-z0-9]+", RESUME.lower()) rather than
#      .split() - see the warning below.
#   e. Sort by weight, highest first, and print them.

# TODO: import re at the top of the file
# TODO: vocabulary = vectorizer.get_feature_names_out()
# TODO: job_weights = vectors[1].toarray()[0]
# TODO: resume_words = set(re.findall(r"[a-z0-9]+", RESUME.lower()))
# TODO: build a list of (word, weight) pairs where weight > 0.1
# TODO:      and the word is not in resume_words
# TODO: sort that list by weight, descending
# TODO: print the words

# WHY re.findall AND NOT .split():
#   .split() breaks on spaces only, so the resume gives you "pandas." and
#   "Flask," with their punctuation still attached. Those never match the
#   vectorizer's clean "pandas" and "flask", and the tool cheerfully reports
#   three skills as missing that are sitting right there in the resume.
#   Try it both ways and watch the list get three items longer.


# ----------------------------------------------------------------------
# IF YOU FINISH EARLY
# ----------------------------------------------------------------------
#   1. Swap in your OWN resume text and see what score you get.
#   2. Add the missing keywords to the resume and re-run. How high can you
#      push the score before the resume stops being honest?
#   3. Print the score as a percentage instead: {match_score:.0%}
