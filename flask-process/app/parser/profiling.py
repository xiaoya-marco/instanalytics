import numpy as np
from app.parser import json_parser as parser
from app.parser import json_comment_parser as comment_parser
from app.parser import json_post_parser as post_parser
import datetime
import re

captionField              = []
captionText         = []
post_num_like                               = []
post_preview_num_like                       = []
post_gating_info                            = []
post_fact_check_overall_rating              = []
post_fact_check_information                 = []
datep                                       = []
hour_vect                                   = np.zeros(24)
timestamp                                   = []
post_number                                 = 0
post_location                               = []
post_is_video                               = []
post_owner_id                               = []
post_owner_username                         = []
postShortcode                               = []
postUrl                                     = []
captionHashtag                              = []
captionTag                                  = []
post_type_name                              = []
postId                                      = []
post_comment_count                          = []
post_comments_disabled                      = []
post_taken_at_timestamp                     = []
post_dimensions_height                      = []
post_dimensions_width                       = []
postShortcodeUrl                            = []
comment_id                                  = []
comment_text                                = []
comment_created_at                          = []
comment_owner_id                            = []
comment_owner_username                      = []
comment_hashtag                             = []
comment_tag                                 = []
list_post_id                                = []
list_post_typename                          = []
list_post_edge_media_to_caption_shortcode   = []
list_post_edge_media_to_comment             = []
list_post_comment_count                     = []
list_post_comment_disbled                   = []
list_post_taken_at_timestamp                = []
list_post_dimensions                        = []
list_post_width                             = []
list_post_height                            = []
list_post_display_url                       = []
list_post_edge_media_preview_like           = []
list_post_edge_media_preview_like_count     = []
list_post_edge_media_to_caption_text        = []
list_post_text_tag                          = []
list_post_text_hashtag                      = []
list_post_owner                             = []
list_post_owner_id                          = []
list_post_thumbnail_src                     = []
list_post_is_video                          = []
list_video_view_count                       = []

def loadLists(info):
    for edge in parser.get_edges(info):
        ''' Location's posts'''
        post_location.append(parser.post_location(edge))

        ''' Video'''
        post_is_video.append(parser.post_is_video(edge))

        ''' Owner's posts '''
        post_owner_id.append(parser.post_owner_id(edge))
        post_owner_username.append(parser.post_owner_username(edge))

        ''' Caption's posts '''
        captionField.append(parser.post_edge_media_to_caption(edge))
        if not captionField[-1]:
            captionText.append("")
        else:
            captionText.append(parser.post_edge_media_to_caption_text(edge))
        if edge:
            ''' Hashtag in caption'''
            text    = parser.post_edge_media_to_caption_text(edge)
            regex   = r"#[^ #]+"
            matches = [match.group() for match in re.finditer(regex, text, re.MULTILINE)]
            captionHashtag.append(matches)
            ''' Tag in caption'''
            text    = parser.post_edge_media_to_caption_text(edge)
            regex   = r"@[^ @]+"
            matches = [match.group() for match in re.finditer(regex, text, re.MULTILINE)]
            captionTag.append(matches)
        else:
            captionHashtag.append(" ")
            captionTag.append(" ")

        ''' Post: shortcode - url - id  '''
        postShortcode.append(parser.shortcode_list(edge))
        postUrl.append(parser.shortcode_url(edge))
        postShortcodeUrl.append((parser.shortcode_list(edge), parser.shortcode_url(edge)))
        postId.append(parser.post_id(edge))

        ''' Post type '''
        post_type_name.append(parser.post_typename(edge))

        ''' Post: comment - like '''
        post_comment_count.append(parser.post_comment_count(edge))
        post_comments_disabled.append(parser.post_comments_disabled(edge))
        post_num_like.append(parser.post_num_like(edge))
        post_preview_num_like.append(parser.post_preview_num_like(edge))

        ''' Date's posts '''
        date = datetime.datetime.fromtimestamp(parser.post_taken_at_timestamp(edge))

        ''' Dimensions' posts '''
        post_dimensions_height.append(parser.post_dimensions_height(edge))
        post_dimensions_width.append(parser.post_dimensions_width(edge))

        ''' Other info '''
        post_gating_info.append(parser.post_gating_info(edge))
        post_fact_check_overall_rating.append(parser.post_fact_check_overall_rating(edge))
        post_fact_check_information.append(parser.post_fact_check_information(edge))
        hour = int(date.strftime('%H'))
        hour_vect[hour] += parser.post_num_like(edge)
        datep.append(hour)


def reset_profile_post_1():
    global post_location
    global post_is_video
    global post_owner_id
    global post_owner_username
    post_location                            = []
    post_is_video                            = []
    post_owner_id                            = []
    post_owner_username                      = []


def reset_profile_post():
    global postShortcode
    global postShortcodeUrl
    global postUrl
    global captionHashtag
    global captionTag
    global post_type_name
    global postId
    global post_comment_count
    global post_comments_disabled
    global post_taken_at_timestamp
    global post_dimensions_height
    global post_dimensions_width
    postShortcode                           = []
    postShortcodeUrl                      = []
    postUrl                                 = []
    captionHashtag                          = []
    captionTag                              = []
    post_type_name                          = []
    postId                                  = []
    post_comment_count                      = []
    post_comments_disabled                  = []
    post_taken_at_timestamp                 = []
    post_dimensions_height                  = []
    post_dimensions_width                   = []


''' Called by get_profile '''


def get_shortcode_list():
    return postShortcode, postUrl


def get_shortcode_url_list():
    return postShortcodeUrl


def get_post_type_name():
    return post_type_name


def get_post_id():
    return postId


def get_post_comment_count():
    return post_comment_count


def get_post_comments_disabled():
    return post_comments_disabled


def get_post_taken_at_timestamp():
    return post_taken_at_timestamp


def get_post_dimensions():
    return post_dimensions_height, post_dimensions_width


def get_post_location():
    return post_location


def post_get_post_is_video():
    return list_post_is_video


def get_post_like():
    return post_num_like, post_preview_num_like


def post_get_post_owner_id():
    return list_post_owner_id


def get_post_data2():
    return post_gating_info, post_fact_check_overall_rating, post_fact_check_information


def post_found_hashtag():
    return captionHashtag


def post_found_tag():
    return captionTag


def get_timestamp():
    for i in range(0, 24):
        timestamp.append(hour_vect[i])
    return timestamp, datep

def get_post_text():
    return captionText


def reset_comment():
    global comment_id
    global comment_text
    global comment_created_at
    global comment_owner_id
    global comment_owner_username
    global comment_hashtag
    global comment_tag
    comment_id                   = []
    comment_text                 = []
    comment_created_at           = []
    comment_owner_id             = []
    comment_owner_username       = []
    comment_hashtag              = []
    comment_tag                  = []


def comment_for_function(data):
     for comment in comment_parser.comment_post_edge_media_to_comment(data):
        comment_id.append(comment_parser.comment_id(comment))
        comment_text.append(comment_parser.comment_text(comment))
        comment_created_at.append(comment_parser.comment_created_at(comment))
        comment_owner_id.append(comment_parser.comment_owner_id(comment))
        comment_owner_username.append(comment_parser.comment_owner_username(comment))
        try:
            if comment_text[-1]:
                regex = r"@[^ @]+"
                matches = [match.group() for match in re.finditer(regex, comment_text[-1], re.MULTILINE)]
                comment_tag.append(matches)

                regex = r"#[^ #]+"
                matches = [match.group() for match in re.finditer(regex, comment_text[-1], re.MULTILINE)]
                comment_hashtag.append(matches)
            else:
                comment_tag.append(" ")

                comment_hashtag.append(" ")
        except IndexError:
            print('out of limits')


def get_comment_has_next_page(data):
    comment_has_next_page = comment_parser.comment_has_next_page(data)
    return comment_has_next_page


def get_comment_id():
    return comment_id


def get_comment_text():
    return comment_text


def get_comment_created_at():
    return comment_created_at


def get_comment_owner_id():
    return comment_owner_id


def get_comment_owner_username():
    return comment_owner_username


''' Found Comment tag'''


def comment_found_tag():
    return comment_tag


''' Found Comment tag'''


def comment_found_hashtag():
    return comment_hashtag


''' POST DATA'''


def post_get_post_count(info):
    post_count = post_parser.post_count(info)
    return post_count


def post_get_post_page_info_has_next_page(info):
    post_page_info_has_next_page = post_parser.post_page_info_has_next_page(info)
    return post_page_info_has_next_page


def post_get_post_page_info_end_cursor(info):
    post_page_info_end_cursor = post_parser.post_page_info_end_cursor(info)
    return post_page_info_end_cursor


def post_get_post_edges(info):
    post_edges = post_parser.post_edges(info)
    return post_edges


def reset_post():
    global list_post_id
    global list_post_typename
    global list_post_edge_media_to_caption_shortcode
    global list_post_edge_media_to_comment
    global list_post_comment_count
    global list_post_comment_disbled
    global list_post_taken_at_timestamp
    global list_post_dimensions
    global list_post_width
    global list_post_height
    global list_post_display_url
    global list_post_edge_media_preview_like
    global list_post_edge_media_preview_like_count
    global list_post_edge_media_to_caption_text
    global list_post_text_tag
    global list_post_text_hashtag
    global list_post_owner
    global list_post_owner_id
    global list_post_thumbnail_src
    global list_post_is_video
    global list_video_view_count
    list_post_id                                       = []
    list_post_typename                                 = []
    list_post_edge_media_to_caption_shortcode          = []
    list_post_edge_media_to_comment                    = []
    list_post_comment_count                            = []
    list_post_comment_disbled                          = []
    list_post_taken_at_timestamp                       = []
    list_post_dimensions                               = []
    list_post_width                                    = []
    list_post_height                                   = []
    list_post_display_url                              = []
    list_post_edge_media_preview_like                  = []
    list_post_edge_media_preview_like_count            = []
    list_post_edge_media_to_caption_text               = []
    list_post_text_tag                                 = []
    list_post_text_hashtag                             = []
    list_post_owner                                    = []
    list_post_owner_id                                 = []
    list_post_thumbnail_src                            = []
    list_post_is_video                                 = []
    list_video_view_count                              = []


def post_for_function(info, n):
    post_preview = len(post_parser.post_edges(info))

    for edge in parser.get_edges(info):
        list_post_id.append(post_parser.post_id(edge))
        list_post_typename.append(post_parser.post_typename(edge))
        list_post_edge_media_to_caption_shortcode.append(post_parser.post_edge_media_to_caption_shortcode(edge))
        list_post_edge_media_to_comment.append(post_parser.post_edge_media_to_comment(edge))
        if list_post_edge_media_to_comment[-1]:
            list_post_comment_count.append(post_parser.post_edge_media_to_comment_count(edge))
        else:
            list_post_comment_count.append(" ")
        list_post_comment_disbled.append(post_parser.post_comment_disabled(edge))
        list_post_taken_at_timestamp.append(post_parser.post_taken_at_timestamp(edge))
        list_post_dimensions.append(post_parser.post_dimensions(edge))
        if list_post_dimensions[-1]:
            list_post_width.append(post_parser.post_width(edge))
            list_post_height.append(post_parser.post_height(edge))
        else:
            list_post_width.append(" ")
            list_post_height.append(" ")
        list_post_display_url.append(post_parser.post_display_url(edge))
        list_post_edge_media_preview_like.append(post_parser.post_edge_media_preview_like(edge))
        if list_post_edge_media_preview_like[-1]:
            list_post_edge_media_preview_like_count.append(post_parser.post_edge_media_preview_like_count(edge))
        else:
            list_post_edge_media_preview_like_count.append(" ")
        if list_post_edge_media_to_caption_text[-1]:
            regex = r"@[^ @]+"
            matches = [match.group() for match in re.finditer(regex, list_post_edge_media_to_caption_text[-1], re.MULTILINE)]
            list_post_text_tag.append(matches)

            regex = r"#[^ #]+"
            matches = [match.group() for match in re.finditer(regex, list_post_edge_media_to_caption_text[-1], re.MULTILINE)]
            list_post_text_hashtag.append(matches)
        else:
            list_post_text_tag.append(" ")
            list_post_text_hashtag.append(" ")
        list_post_owner.append(post_parser.post_owner(edge))
        if list_post_owner[-1]:
            list_post_owner_id.append(post_parser.post_owner_id(edge))
        else:
            list_post_owner_id.append(" ")
        list_post_thumbnail_src.append(post_parser.post_thumbnail_src(edge))
        list_post_is_video.append(post_parser.post_is_video(edge))
        if list_post_is_video[-1]:
            list_video_view_count.append(post_parser.post_video_view_count(edge))
        else:
            list_video_view_count.append(" ")


def post_get_post_id():
    return list_post_id


def post_get_post_typename():
    return list_post_typename


def post_get_post_edge_media_to_caption_edges(info):
    list_post_edge_media_to_caption_edges = []
    post_preview = len(post_parser.post_edges(info))
    for i in range(0, post_preview):
        list_post_edge_media_to_caption_edges.append(post_parser.post_edge_media_to_caption_edges(info, i))
    return list_post_edge_media_to_caption_edges


def post_get_post_text(info):
    post_edge_media_to_caption_edges = post_get_post_edge_media_to_caption_edges(info)
    for edge in parser.get_edges(info):
        if not edge:
            list_post_edge_media_to_caption_text.append(" ")
        else:
            list_post_edge_media_to_caption_text.append(post_parser.post_edge_media_to_caption_text(edge))
    return list_post_edge_media_to_caption_text


''' SONO UTILI?'''


def post_get_post_edge_media_to_caption_shortcode():
    return list_post_edge_media_to_caption_shortcode


def post_get_post_edge_media_to_comment_count():
    return list_post_comment_count


def post_get_post_comment_disabled():
    return list_post_comment_disbled


def post_get_post_taken_at_timestamp():
    return list_post_taken_at_timestamp


def post_get_post_dimensions():
    return list_post_width, list_post_height


def post_get_post_display_url():
    return list_post_display_url


def post_get_post_preview_like_count():
    return list_post_edge_media_preview_like_count


def post_get_post_tag():
    return list_post_text_tag


def post_get_post_hashtag():
    return list_post_text_hashtag


def post_get_list_post_thumbnail_src():
    return list_post_thumbnail_src


def post_get_post_video_view_count():
    return list_video_view_count


def get_post_is_video():
    return post_is_video


def get_post_owner():
    return post_owner_id, post_owner_username