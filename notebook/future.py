# ENTER_EXIT = rule(
#     rule(
#         normalized('работать').optional(),
#         eq('только').optional(),
#         or_(
#             eq('на'),
#             eq('для'),
#             eq('в')
#         ),
#     ).optional(),
#     morph_pipeline(['вход', 'выход', 'обычный режим']),
# )

# ENTRANCE = rule(
#     ENTER_EXIT,
#     rule(
#         in_('и/-,').optional(),
#         ENTER_EXIT,
#     ).optional(),
#     normalized('пассажир').optional(),  # пассажирам
# )

# IS_OPEN = morph_pipeline(['открыт', 'закрыт'])

# STATUS = rule(
#     normalized('есть').optional(),  # будет, была
#     or_(
#         rule(ENTRANCE),
#         rule(IS_OPEN, ENTRANCE.optional()),
#         rule(ENTRANCE.optional(), IS_OPEN),
#     ),
# )

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
