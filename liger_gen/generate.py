from lookmlgen.view import View
from lookmlgen.field import Dimension, DimensionGroup, Measure
from lookmlgen.base_generator import GeneratorFormatOptions

from inflection import *


# def __map_column_type(sql_type):
#     if 'BOOLEAN' in str(sql_type):
#         return 'yesno'
#     elif 'NUMERIC' in str(sql_type) or 'INTEGER' in str(sql_type) or 'FLOAT' in str(sql_type):
#         return 'number'
#     elif 'TIMESTAMP' in str(sql_type):
#         return 'time'
#     else:
#         return 'string'
#
# def __map_dimension_field(col):
#     field = None
#     col_type = __map_column_type(col.type)
#
#     if col.name =='id':
#         field = Dimension('id', type=col_type, primary_key=True)
#     elif 'TIMESTAMP' in str(col.type):
#         field = DimensionGroup(col.name)
#     else:
#         field = Dimension(col.name, type=col_type)
#
#     field.description = col.comment
#     return field
#
# def __add_standard_count_measures(table, view):
#     entity_name = humanize(table.name)
#
#     view.add_field(Measure('count', type='count', sql='${id}',
#         description='How many {0} are there?'.format(entity_name)))
#
#     view.add_field(Measure('unique_{0}_count'.format(singularize(table.name)),
#         type='count_distinct',description='How many distinct {0} are there?'.format(entity_name, sql='${id}')))
#
# def __add_count_per_measures(table, view):
#     count_per_cols = [col for col in table.columns if col.name in __COUNT_DISTINCT_ID_COLUMNS]
#
#     for col in count_per_cols:
#         measure_name = 'unique_{0}_count'.format(__COUNT_DISTINCT_ID_COLUMNS[col.name])
#         view.add_field(Measure(measure_name, type='count_distinct',
#             description='How many distinct {0} are there?'.format(__COUNT_DISTINCT_ID_COLUMNS[col.name])
#             , sql='${{{0}}}'.format(col.name)))
#
# def __add_standard_date_measures(table, view):
#     entity_name = humanize(table.name)
#
#     time_cols = [col for col in table.columns if __map_column_type(col.type) is 'time']
#     for tcol in time_cols:
#         #min
#         measure_name = 'first_{0}'.format(tcol.name)
#         description = "When is the first {entity} {action} time?".format(entity=entity_name, action=tcol.name)
#         sql =
#         view.add_field(Measure(measure_name, type='date_time',description=description, sql=
#         #    description='How many distinct {0} are there?'.format(__COUNT_DISTINCT_ID_COLUMNS[col.name])
#         #    , sql='${{{0}}}'.format(col.name)))
#
# def generate_lookml(table, f):
#     view = View(table.name, sql_table_name=table.name)
#
#     #create dimensions from columns
#     for col in table.columns:
#         view.add_field(__map_dimension_field(col))
#
#     __add_standard_count_measures(table, view)
#
#     __add_standard_date_measures(table, view)
#
#     __add_count_per_measures(table, view)
#
#     format_options = GeneratorFormatOptions(view_fields_alphabetical=False,
#                            omit_default_field_type=False,
#                            omit_time_frames_if_not_set=True,
#                            warning_header_comment=None)
#
#     view.generate_lookml(f,format_options)
#
#     return f


class LigerView:
    COUNT_DISTINCT_ID_COLUMNS = {'user_id' : 'users', 'visitor_id' : 'visitors'}
    def __init__(self, table):
        self.table = table
        self.table_name = self.table.name
        self.entity_name = humanize(self.table_name).lower()
        self.format_options = GeneratorFormatOptions(view_fields_alphabetical=False,
                               omit_default_field_type=False,
                               omit_time_frames_if_not_set=True,
                               warning_header_comment=None)
        self.__init_view()

    def __init_view(self):
        self.view = View(self.table_name, sql_table_name=self.table_name)

    def __map_column_type(self, sql_type):
        if 'BOOLEAN' in str(sql_type):
            return 'yesno'
        elif 'NUMERIC' in str(sql_type) or 'INTEGER' in str(sql_type) or 'FLOAT' in str(sql_type):
            return 'number'
        elif 'TIMESTAMP' in str(sql_type):
            return 'time'
        else:
            return 'string'

    def __map_dimension_field(self, col):
        field = None
        col_type = self.__map_column_type(col.type)

        if col.name =='id':
            field = Dimension('id', type=col_type, primary_key=True)
        elif 'TIMESTAMP' in str(col.type):
            field = DimensionGroup(col.name)
        else:
            field = Dimension(col.name, type=col_type)

        field.description = col.comment
        return field

    def __add_measure(self, name, type, sql_col, description, func=None):
        if func:
            sql ='{func}(${{{sql_col}}})'.format(func=func, sql_col=sql_col)
        else:
            sql ='${{{0}}}'.format(sql_col)

        self.view.add_field(Measure(name=name, type=type, sql=sql,description=description))

    def __add_standard_count_measures(self):
        name = 'count'
        type = 'count'
        sql_col ='id'
        description = 'How many {0} are there?'.format(self.entity_name)
        self.__add_measure(name, type, sql_col, description)

        name = 'unique_{0}_count'.format(singularize(self.table_name))
        type = 'count_distinct'
        sql_col ='id'
        description = 'How many distinct {0} are there?'.format(self.entity_name)
        self.__add_measure(name, type, sql_col, description)


    def __add_count_per_measures(self):
        count_per_cols = [col for col in self.table.columns if col.name in self.COUNT_DISTINCT_ID_COLUMNS]

        for col in count_per_cols:
            name = 'unique_{0}_count'.format(self.COUNT_DISTINCT_ID_COLUMNS[col.name])
            type ='count_distinct'
            description='How many distinct {0} are there?'.format(self.COUNT_DISTINCT_ID_COLUMNS[col.name])
            sql_col = col.name
            self.__add_measure(name, type, sql_col, description)


    def __add_standard_date_measures(self):
        time_cols = [col for col in self.table.columns if self.__map_column_type(col.type) is 'time']
        for tcol in time_cols:
            type = 'date_time'
            measure_name = 'first_{0}'.format(tcol.name)
            description = "When is the first {entity} {action} time?".format(
                entity=self.entity_name, action=humanize(tcol.name).lower())
            sql_col = '{0}_raw'.format(tcol.name)
            self.__add_measure(measure_name, type, sql_col, description, func='min')

            measure_name = 'last_{0}'.format(tcol.name)
            description = "When is the last {entity} {action} time?".format(
                entity=self.entity_name, action=humanize(tcol.name).lower())
            self.__add_measure(measure_name, type, sql_col, description, func='max')

    def generate_lookml(self, f):
        self.__init_view() #always start with with a new view

        #create dimensions from columns
        for col in self.table.columns:
            self.view.add_field(self.__map_dimension_field(col))

        self.__add_standard_count_measures()

        self.__add_standard_date_measures()

        self.__add_count_per_measures()

        self.view.generate_lookml(f,self.format_options)

        return f
