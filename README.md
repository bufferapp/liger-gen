# liger-gen

Command line tool for generating Liger compatible LookML using database schema.

This tool can generate a starting LookML view file for the Liger project, following all our naming conventions, best practices and adding all the standard fields. 

It will reflect the schema of the underlying table to figure out which fields to generate.

As a best practice, you should annotate the fields on the database with inline documentation using `comment on` statements, which `liger-gen` will then use for the `description` on fields.

## Setup

Clone the repo

```ssh
git clone https://github.com/bufferapp/liger-gen
cd liger-gen
```

Build the Docker image

```ssh
make build
```

## Usage

Run liger-gen, passing in the table name

```ssh
./liger-gen.sh funnel_tags
```

This will print the output LookML to stdout. To capture the output:

```ssh
./liger-gen.sh funnel_tags | pbcopy #to the clipboard

./liger-gen.sh funnel_tags > funnel_tags.lkml #to a file
```

# Assumptions

liger-gen makes some assumptions that you'll need to follow on your table schema for best results.

- You're following all the Liger naming conventions
- All the data you need Looker dimensions are in columns in your table, ie you don't need a derived table in Looker.
- All table columns have inline documentation using the `column on` statements
- Your table has a Primary Key field named `id`
- Your table is named in such a way that it fully describes the entities it contains. This is useful for auto-generating inline documentation for standard measures. So a table named `funnel_tags` will auto generate a unique count measure called `unique_funnel_tag_count` with a `description` of `How many distinct funnel tags are there?`

## Known issues

There are still a couple of rough edges that need to be fixed. Feel free to add more if you come across them.

- We're not generating all standard measures yet, most notably the standard measures for number dimensions
- The default `count` measure will add a `sql: ${id}` clause that generates a LookML warning. The sql clause is not needed and can just be removed. This will hopefully be fixed soon
- We're not adding comments such as `#DIMENSIONS` or `#MEASURES` in between field type sections
