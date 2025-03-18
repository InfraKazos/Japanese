reserved = {
    "変数": "VAR",
    "関数": "FUNC",
    "場合": "THEN",
    "間": "WHILE",
    "でもそうじゃなければ": "ELSE",
    "回反復": "TIMES_LOOP",
    "値": "VALUE",
    "以下": "BELOW",
    "そして": "CONTINUE",
    "等": "EQUAL",
    "しい": "EQUAL_B",
    "しくない": "NOT_EQUAL_B",
    "大": "GREATER",
    "きい": "GREATER_B",
    "きくない": "NOT_GREATER_B",
    "小": "LESSER",
    "さい": "LESSER_B",
    "さくない": "NOT_LESSER_B"
}

verbs = {
    "代入": "ASSIGN",
    "言": "PRINT",
    "呼": "CALL",
    "返": "RETURN",
    "終": "END",
    "増": "INCREMENT",
    "減": "DECREMENT",
    "入力": "INPUT",
    "整数化": "CONV_INT",
    "文字列化": "CONV_STRING",
    "浮動小数点化": "CONV_FLOAT"
}

base_forms = {
    "代入": "する",
    "返": "す",
    "言": "う",
    "呼": "ぶ",
    "終": "わる",
    "増": "やす",
    "減": "らす",
    "入力": "する",
    "整数化": "する",
    "文字列化": "する",
    "浮動小数点化": "する"
}

te_forms = {
    "代入": "して",
    "返": "して",
    "言": "って",
    "呼": "んで",
    "終": "わって",
    "増": "やして",
    "減": "らして",
    "入力": "して",
    "整数化": "して",
    "文字列化": "して",
    "浮動小数点化": "して"
}

negative_forms = {
    "代入": "しない",
    "言": "わない",
    "返": "さない",
    "呼": "ばない",
    "終": "わらない",
    "増": "やさない",
    "減": "らさない",
    "入力": "しない",
    "整数化": "しない",
    "文字列化": "しない",
    "浮動小数点化": "しない"
}

negative_te_forms = {
    "代入": "しなくて",
    "言": "わなくて",
    "返": "さなくて",
    "呼": "ばなくて",
    "終": "わらなくて",
    "増": "やさなくて",
    "減": "らさなくて",
    "入力": "しなくて",
    "整数化": "する",
    "文字列化": "する"
}

particles = {
    "は": "TOPIC",
    "が": "SUBJECT",
    "の": "POSSESSIVE",
    "を": "OBJECT",
    "と": "QUOTE",
    "という": "CALLED",
    "で": "AT",
    "から": "FROM",
    "まで": "UNTIL",
    "に": "TO",
    "より": "COMPARE"
}

t_PLUS = r"\+"
t_MINUS = r"-"
t_MULTIPLY = r"\*"
t_DIVIDE = r"/"
t_MODULO = r"\%"
t_EXPONENT = r"\^"
t_ignore = " \t\n[a-zA-Z]"

tokens = tuple(particles.values()) + ("EXPONENT", "MODULO", "NUMBER", "VERB_B", "TE_VERB_B", "NEGATIVE_VERB_B", "NEGATIVE_TE_VERB_B", "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "STRING") + tuple(reserved.values()) + tuple(verbs.values())