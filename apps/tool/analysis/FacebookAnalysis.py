import json

from tool.models import Posts,Users

def get_posts(posts):
    node = posts.get('node')
    comet_sections = node.get('comet_sections')
    content = comet_sections.get('content').get('story')
    attachments = content.get('attachments')
    actors = content.get('actors')[0]
    video_list = []
    image_list = []
    posts_object=Posts()
    if content.get('wwwURL'):
        posts_object.posts_url = content.get('wwwURL')
    if len(attachments) != 0:
        for attachment in attachments:
            attachment = attachment.get('styles').get('attachment')
            if attachment.get('media'):
                media = attachment.get('media')
                large_share_image = media.get('large_share_image')
                if large_share_image:
                    image_list.append(large_share_image.get('uri'))
                if media.get('browser_native_hd_url') == None or media.get('browser_native_hd_url') == '':
                    if media.get('browser_native_sd_url') != None:
                        video_list.append(media.get('browser_native_sd_url'))
                else:
                    video_list.append(media.get('browser_native_hd_url'))

                if media.get('photo_image'):
                    photo_image = media.get('photo_image')
                    image_list.append(photo_image.get('uri'))
                if media.get('url') and posts_object.posts_url == None or posts_object.posts_url == '':
                    posts_object.posts_url = media.get('url')
            else:
                if attachment.get('all_subattachments'):
                    for subattachment in attachment.get('all_subattachments').get('nodes'):
                        media = subattachment.get('media')
                        if media:
                            if media.get('image'):
                                image = media.get('image')
                                image_list.append(image.get('uri'))
                                if media.get('url') and posts_object.posts_url == None or posts_object.posts_url == '':
                                    posts_object.posts_url = media.get('url')
    elif content.get('comet_sections'):
        comet_sections = content.get('comet_sections')
        if comet_sections.get('attached_story'):
            attached_story = comet_sections.get('attached_story')
            if attached_story.get('story'):
                story = attached_story.get('story')
                if story.get('attached_story'):
                    attached_story = story.get('attached_story')
                    if attached_story.get('comet_sections'):
                        comet_sections = attached_story.get('comet_sections')
                        if comet_sections.get('attached_story_layout'):
                            attached_story_layout = comet_sections.get('attached_story_layout')
                            if attached_story_layout.get('story'):
                                story = attached_story_layout.get('story')
                                attachments = story.get('attachments')
                                for attachment in attachments:
                                    if attachment.get('styles'):
                                        styles = attachment.get('styles')
                                        if styles.get('attachment'):
                                            attachment = styles.get('attachment')
                                            if attachment.get('media'):
                                                media = attachment.get('media')
                                                large_share_image = media.get('large_share_image')
                                                if large_share_image:
                                                    image_list.append(large_share_image.get('uri'))

                                            if attachment.get('subattachments'):
                                                subattachments = attachment.get('subattachments')
                                                for subattachment in subattachments:
                                                    multi_share_media_card_renderer = subattachment.get('multi_share_media_card_renderer')
                                                    if multi_share_media_card_renderer:
                                                        attachment = multi_share_media_card_renderer.get('attachment')
                                                        if attachment:
                                                            media = attachment.get('media')
                                                            large_share_image = media.get('large_share_image')
                                                            if large_share_image:
                                                                image_list.append(large_share_image.get('uri'))

                                                            if media.get('browser_native_hd_url') == None or media.get(
                                                                    'browser_native_hd_url') == '':
                                                                if media.get('browser_native_sd_url') != None:
                                                                    video_list.append(media.get('browser_native_sd_url'))
                                                            else:
                                                                video_list.append(media.get('browser_native_hd_url'))

                                                            if media.get('preferred_thumbnail'):
                                                                preferred_thumbnail = media.get('preferred_thumbnail')
                                                                if preferred_thumbnail:
                                                                    photo_image = preferred_thumbnail.get('image')
                                                                    if photo_image:
                                                                        image_list.append(photo_image.get('uri'))

    if Posts.objects.filter(post_id=node.get('post_id')).first():
        return
    posts_object.post_id = node.get('post_id')
    if content.get('message'):
        message = content.get('message')
        if message.get('text'):
            posts_object.message = message.get('text')
    else:
        posts_object.message = ''
    users= Users.objects.filter(id=actors.get('id')).first()
    if not users:
        users = Users(id=actors.get('id'), name=actors.get('name'), url=actors.get('url'))
        users.save()
    posts_object.users = users
    posts_object.feedback_id = node.get('feedback').get('id')
    posts_object.video_list = json.dumps(video_list,ensure_ascii=False)
    posts_object.image_list = json.dumps(image_list,ensure_ascii=False)
    posts_object.source_data = json.dumps(node)
    posts_object.save()


def set_uaers(data):
    if 'viewer' in data:
        viewer = data['viewer']
        if 'bootstrap_keywords' in viewer:
            bootstrap_keywords = viewer['bootstrap_keywords']
            if 'edges' in bootstrap_keywords:
                for edge in bootstrap_keywords['edges']:
                    users=Users()
                    node = edge['node']
                    sts_info = node['sts_info']
                    if sts_info:
                        direct_nav_result = sts_info['direct_nav_result']
                        if direct_nav_result:
                            if not 'FRIEND' == direct_nav_result['type']:
                                continue
                            if Users.objects.filter(id=users.id).first():
                                continue
                            users.id = direct_nav_result['ent_id']
                            users.img_url = direct_nav_result['img_url']
                            users.url = direct_nav_result['link_url']
                            users.name = direct_nav_result['title']
                            users.source_data = json.dumps(direct_nav_result)
                            users.save()

    elif 'node' in data:
        node = data['node']
        if 'pageItems' in node:
            pageItems = node['pageItems']
            if 'edges' in pageItems:
                for edge in pageItems['edges']:
                    id= edge['node']['node']['id']
                    if Users.objects.filter(id=id).first():
                        continue
                    users = Users()
                    users.id = id
                    users.img_url = edge['node']['image']['uri']
                    users.url = edge['node']['url']
                    users.name = edge['node']['title']['text']
                    users.source_data = json.dumps(edge)
                    users.save()