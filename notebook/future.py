# SENTENCE = or_(
#     rule(TIME.optional(), STATUS, STATION_OR_TRANSFER),
#     rule(TIME.optional(), STATION_OR_TRANSFER, STATUS),
#     rule(STATION_OR_TRANSFER, STATUS, TIME.optional()),
#     rule(STATUS, STATION_OR_TRANSFER, TIME.optional()),
# )

# parser = Parser(SENTENCE)
# seed(1)
# for line in sample(texts, 50):
#     matches = list(parser.findall(line))
#     spans = [_.span for _ in matches]
#     show_markup(line, spans)

#     if matches:
#         match = matches[0]
#         display(match.tree.as_dot)
