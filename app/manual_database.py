user = Table(
    "user",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("username", String(50), unique=True, index=True),
    Column("user_password", String),
    Column("user_mail", String),
    Column("user_type", String),
)

take = Table(
    "take",
    metadata,
    Column("user_id", Integer, primary_key=True, ForeignKey('user.user_id')),
    Column("quiz_id", Integer, primary_key=True, ForeignKey('question.question_id')),
    Column("date_passage", Datetime),
    Column("score", Integer),
    Column("nbr_attempts", Integer)
)

status = Table(
    "status",
    Column("status_id", Integer, primary_key=True),
    Column("label", String),
    Column("description", String)
)

Visibility = Table(
    "visibility",
    Column("visibility_id", Integer, primary_key=True),
    Column("label", String),
    Column("description", String)
)

Category = Table(
    "category",
    Column("category_id", Integer, primary_key=True),
    Column("title", String),
    Column("description", String)
)

question = Table(
    "question",
    Column("question_id", Integer, primary_key=True),
    Column("question_text", String),
)

answer = Table(
    "answer",
    Column("answer_id", Integer, primary_key=True),
    Column("answer_text", String),
    Column("quest_id", Integer, ForeignKey('question.question_id'))
)

consists = Table(
    "consists"
    Column("quest_id", Integer, primary_key=True, ForeignKey('question.question_id')),
    Column("quiz_id", Integer, primary_key=True, ForeignKey('answer.answer_id')),
)

Quizz = Table(
    "quizz",
    Column("quiz_id", Integer, primary_key=True),
    Column("title", String),
    Column("description", String),
    Column("duration_min", Integer),
    Column("maxNbrAttempts", Integer),
    Column("date_creation", Datetime),
    Column("dateLastModif", Datetime),
    Column("status_id", Integer, ForeignKey('status.status_id')),
    Column("category_id", Integer, ForeignKey('Category.category_id')),
    Column("visibility_id", Integer, ForeignKey('Visibility.visibility_id')),
    Column("admin_id", Integer, ForeignKey('user.user_id')),
)
