#!/usr/bin/python
# -*- coding: utf-8 -*-


def index_definition(doc_type):
    return {
        "mappings": {
            doc_type: {
                "properties": {
                    "title": {
                        "type": "string",
                        "analyzer": "kuromoji",
                    },
                    "content": {
                        "type": "string",
                        "analyzer": "kuromoji",
                    },
                    "category": {
                        "type": "string",
                        "analyzer": "kuromoji",
                    },
                    "slug": {
                        "type": "string",
                        "analyzer": "english"
                    },
                    "pub_date": {
                        "type": "date",
                        "format": "dateOptionalTime"
                    }
                }
            }
        }
    }


def kuromoji_analyzer_def():
    return {
        "analysis": {
            "filter": {
                "kuromoji_rf": {
                    "type": "kuromoji_readingform",
                    "use_romaji": "true"
                },
                "kuromoji_pos": {
                    "type": "kuromoji_part_of_speech",
                    "enable_position_increment": "false",
                    "stoptags": ["# verb-main:", "動詞-自立"]
                },
                "kuromoji_ks": {
                    "type": "kuromoji_stemmer",
                    "minimum_length": 6
                }
            },
            "tokenizer": {
                "kuromoji": {
                    "type": "kuromoji_tokenizer"
                }
            },
            "analyzer": {
                "kuromoji_analyzer": {
                    "type": "custom",
                    "tokenizer": "kuromoji_tokenizer"
                }
            }
        }
    }


def search_query_body(query):
    return {
        'query': {
            'multi_match': {
                'query': query,
                'fields': ['title', 'slug', 'content', 'category']
            }
        },
        'highlight': {
            'fields': {
                'title': {},
                'slug': {},
                'content': {},
                'category': {},
            }
        }
    }
