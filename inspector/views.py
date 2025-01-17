# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from collections import OrderedDict

import lorem
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from lti import ToolConfig

logger = logging.getLogger(__name__)


# Create your views here.

VARIABLE_EXPANSIONS = [
    'Caliper.url',
    'Canvas.account.id',
    'Canvas.account.name',
    'Canvas.account.sisSourceId',
    'Canvas.api.baseUrl',
    'Canvas.api.collaborationMembers.url',
    'Canvas.api.domain',
    'Canvas.assignment.dueAt',
    'Canvas.assignment.dueAt.iso8601',
    'Canvas.assignment.id',
    'Canvas.assignment.lockAt',
    'Canvas.assignment.lockAt.iso8601',
    'Canvas.assignment.pointsPossible',
    'Canvas.assignment.published',
    'Canvas.assignment.title',
    'Canvas.assignment.unlockAt',
    'Canvas.assignment.unlockAt.iso8601',
    'Canvas.course.id',
    'Canvas.course.name',
    'Canvas.course.previousContextIds',
    'Canvas.course.previousContextIds.recursive',
    'Canvas.course.previousCourseIds',
    'Canvas.course.sectionIds',
    'Canvas.course.sectionSisSourceIds',
    'Canvas.course.sisSourceId',
    'Canvas.course.startAt',
    'Canvas.course.workflowState',
    'Canvas.css.common',
    'Canvas.enrollment.enrollmentState',
    'Canvas.externalTool.url',
    'Canvas.file.media.duration',
    'Canvas.file.media.id',
    'Canvas.file.media.size',
    'Canvas.file.media.title',
    'Canvas.file.media.type',
    'Canvas.file.usageRights.copyrightText',
    'Canvas.file.usageRights.name',
    'Canvas.file.usageRights.url',
    'Canvas.group.contextIds',
    'Canvas.logoutService.url',
    'Canvas.masqueradingUser.id',
    'Canvas.masqueradingUser.userId',
    'Canvas.membership.concludedRoles',
    'Canvas.membership.roles',
    'Canvas.module.id',
    'Canvas.moduleItem.id',
    'Canvas.rootAccount.id',
    'Canvas.rootAccount.sisSourceId',
    'Canvas.root_account.global_id',
    'Canvas.root_account.id',
    'Canvas.root_account.sisSourceId',
    'Canvas.shard.id',
    'Canvas.term.name',
    'Canvas.term.startAt',
    'Canvas.user.globalId',
    'Canvas.user.id',
    'Canvas.user.isRootAccountAdmin',
    'Canvas.user.loginId',
    'Canvas.user.prefersHighContrast',
    'Canvas.user.sisIntegrationId',
    'Canvas.user.sisSourceId',
    'Canvas.xapi.url',
    'Canvas.xuser.allRoles',
    'Context.id',
    'Context.sourcedId',
    'Context.title',
    'CourseOffering.sourcedId',
    'CourseSection.sourcedId',
    'LtiLink.custom.url',
    'Membership.role',
    'Message.documentTarget',
    'Message.locale',
    'Person.address.timezone',
    'Person.email.primary',
    'Person.name.display',
    'Person.name.family',
    'Person.name.full',
    'Person.name.given',
    'Person.sourcedId',
    'ToolConsumerInstance.guid',
    'ToolConsumerProfile.url',
    'ToolProxy.custom.url',
    'ToolProxyBinding.custom.url',
    'ToolProxyBinding.memberships.url',
    'User.id',
    'User.image',
    'User.username',
    'com.Instructure.membership.roles',
    'com.instructure.Assignment.anonymous_grading',
    'com.instructure.Assignment.lti.id',
    'com.instructure.Course.groupIds',
    'com.instructure.Editor.contents',
    'com.instructure.Editor.selection',
    'com.instructure.File.id',
    'com.instructure.Group.id',
    'com.instructure.Group.name',
    'com.instructure.OriginalityReport.id',
    'com.instructure.Person.name_sortable',
    'com.instructure.PostMessageToken',
    'com.instructure.Submission.id',
    'com.instructure.User.allRoles',
    'com.instructure.brandConfigJS.url',
    'com.instructure.brandConfigJSON',
    'com.instructure.brandConfigJSON.url',
    'com.instructure.contextLabel',
    'vnd.Canvas.OriginalityReport.url',
    'vnd.Canvas.Person.email.sis',
    'vnd.Canvas.root_account.uuid',
    'vnd.Canvas.submission.history.url',
    'vnd.Canvas.submission.url',
    'vnd.instructure.Course.uuid',
    'vnd.instructure.User.uuid',
]

CONTENT_ITEM_TEMPLATE = '{{  \
    "@context": "http://purl.imsglobal.org/ctx/lti/v1/ContentItem",  \
    "@graph": [  \
        {{  \
            "@type": "LtiLinkItem",  \
            "@id": "{}",  \
            "url": "{}",  \
            "title": "{}",  \
            "text": "{}",  \
            "mediaType": "application/vnd.ims.lti.v1.ltilink",  \
            "placementAdvice": {{  \
                "presentationDocumentTarget": "iframe",  \
                "displayHeight": "600", \
                "displayWidth": "100%" \
            }}  \
        }}  \
    ]  \
}}'


def tool_config(request):

    # basic stuff
    app_title = 'LTI Inspector'
    app_description = 'A simple LTI App that echoes the launch parameters'
    launch_view_name = 'lti_launch'
    launch_url = request.build_absolute_uri(reverse(launch_view_name, args=('',)))

    icon_url = request.build_absolute_uri(static('harvard-shield-30-2x.png'))

    # maybe you've got some extensions
    extensions = {
        'canvas.instructure.com': {
            # extension settings...
            'privacy_level': 'public',
            'custom_fields': {},
            'course_navigation': {
                'url': '{}/course_navigation'.format(launch_url),
                'text': '{} - course_navigation'.format(app_title),
                'icon_url': icon_url,
                'visibility': 'public',
                'default': 'enabled',
                'enabled': 'true',
            },
            'account_navigation': {
                'url': '{}/account_navigation'.format(launch_url),
                'text': '{} - account_navigation'.format(app_title),
                'visibility': 'public',
                'default': 'enabled',
                'enabled': 'true',
            },
            'user_navigation': {
                'url': '{}/user_navigation'.format(launch_url),
                'text': '{} - user_navigation'.format(app_title),
                'visibility': 'public',
                'default': 'enabled',
                'enabled': 'true',
            },
            'global_navigation': {
                'url': '{}/global_navigation'.format(launch_url),
                'text': '{} - global_navigation'.format(app_title),
                'visibility': 'public',
                'default': 'enabled',
                'enabled': 'true',
            },
            'course_home_sub_navigation': {
                'url': '{}/course_home_sub_navigation'.format(launch_url),
                'text': '{} - course_home_sub_navigation'.format(app_title),
                'icon_url': icon_url,
                'canvas_icon_class': 'icon-lti',
            },
            'course_settings_sub_navigation': {
                'url': '{}/course_settings_sub_navigation'.format(launch_url),
                'text': '{} - course_settings_sub_navigation'.format(app_title),
                'canvas_icon_class': 'icon-standards',
            },
            'homework_submission': {
                'url': '{}/homework_submission'.format(launch_url),
                'text': '{} - homework_submission'.format(app_title),
                'icon_url': icon_url,
                'message_type': 'ContentItemSelectionRequest',
                'selection_width': '800',
                'selection_height': '600',
                'enabled': 'true',
            },
            'assignment_selection': {
                'url': '{}/assignment_selection'.format(launch_url),
                'text': '{} - assignment_selection'.format(app_title),
                'message_type': 'ContentItemSelectionRequest',
                'icon_url': icon_url,
                'selection_width': '800',
                'selection_height': '600',
                'enabled': 'true',
            },
            'editor_button': {
                'url': '{}/editor_button'.format(launch_url),
                'text': '{} - editor_button'.format(app_title),
                'message_type': 'ContentItemSelectionRequest',
                'icon_url': icon_url,
                'selection_width': '800',
                'selection_height': '600',
                'enabled': 'true',
            },
            'link_selection': {
                'url': '{}/link_selection'.format(launch_url),
                'text': '{} - link_selection'.format(app_title),
                'icon_url': icon_url,
                'message_type': 'ContentItemSelectionRequest',
                'selection_width': '800',
                'selection_height': '600',
                'enabled': 'true',
            },
            'resource_selection': {
                'url': '{}/resource_selection'.format(launch_url),
                'text': '{} - resource_selection'.format(app_title),
                'icon_url': icon_url,
                'selection_width': '800',
                'selection_height': '600',
                'enabled': 'true',
            },
            'tool_configuration': {
                'url': '{}/tool_configuration'.format(launch_url),
                'text': '{} - tool_configuration'.format(app_title),
                'selection_width': '800',
                'selection_height': '600',
                'enabled': 'true',
            },
            'file_menu': {
                'url': '{}/file_menu'.format(launch_url),
                'text': '{} - file_menu'.format(app_title),
            },
        }
    }

    for varname in VARIABLE_EXPANSIONS:
        extensions['canvas.instructure.com']['custom_fields'][varname] = '${}'.format(varname)

    lti_tool_config = ToolConfig(
        title=app_title,
        launch_url=launch_url,
        secure_launch_url=launch_url,
        extensions=extensions,
        description=app_description
    )

    return HttpResponse(lti_tool_config.to_xml(), content_type='text/xml')


@xframe_options_exempt
@csrf_exempt
def lti_launch(request, placement="generic"):

    launch_params = OrderedDict()
    for k in sorted(request.POST.dict().keys()):
        launch_params[k] = request.POST[k]

    lti_message_type = launch_params.get('lti_message_type')

    common_css = None
    if launch_params.get('custom_canvas_css_common'):
        common_css = launch_params.get('custom_canvas_css_common')

    if lti_message_type == 'ContentItemSelectionRequest':
        # we need to let the user choose a piece of content that will be returned
        # as a content-item
        if placement == 'assignment_selection':
            return render(request, 'inspector/assignment_selection.html', {'launch_params': launch_params, 'common_css': common_css})
        elif placement == 'homework_submission':
            return render(request, 'inspector/homework_submission.html', {'launch_params': launch_params, 'common_css': common_css})
        elif placement == 'editor_button':
            logger.debug(launch_params)
            return render(request, 'inspector/editor_selection.html', {'launch_params': launch_params, 'common_css': common_css})

    else:
        return render(
            request,
            'inspector/lti_launch.html',
            {
                'launch_params': launch_params,
                'placement': placement,
                'common_css': common_css,
                'build_info': settings.BUILD_INFO,
            }
        )


@xframe_options_exempt
def return_assignment_selection(request):
    context = {}
    assignment_id = request.POST['assignment_id']
    assignment_url = request.build_absolute_uri(reverse('view_assignment', args=(assignment_id,)))
    title = 'Title for {}'.format(assignment_id)
    description = 'Description for {}'.format(assignment_id)
    context['content_item_return_url'] = request.POST['content_item_return_url']
    context['lti_version'] = 'LTI-1p0'
    context['lti_message_type'] = 'ContentItemSelection'
    context['data'] = request.POST['data']
    context['content_items'] = CONTENT_ITEM_TEMPLATE.format(
        assignment_url,
        assignment_url,
        title,
        description,
    )

    return render(request, 'inspector/return_assignment_selection.html', context)


@xframe_options_exempt
def return_editor_button_selection(request):
    context = {}
    placement = 'editor_button'
    # extra_param = request.POST['extra_param']
    content_url = request.build_absolute_uri(reverse('lti_launch', args=('',)))
    title = 'Tool-provided embed content'
    description = 'This content is provided by an LTI tool.'
    context['content_item_return_url'] = request.POST['content_item_return_url']
    context['lti_version'] = 'LTI-1p0'
    context['lti_message_type'] = 'ContentItemSelection'
    context['data'] = request.POST['data']
    context['content_items'] = CONTENT_ITEM_TEMPLATE.format(
        content_url,
        content_url,
        title,
        description,
    )
    context['placement'] = placement
    return render(request, 'inspector/return_editor_button_selection.html', context)


@xframe_options_exempt
def return_homework_submission(request):
    context = {}
    submission_id = request.POST['submission_id']
    submission_url = request.build_absolute_uri(reverse('view_submission', args=(submission_id,)))
    title = 'Title for {}'.format(submission_id)
    description = 'Description for {}'.format(submission_id)
    context['content_item_return_url'] = request.POST['content_item_return_url']
    context['lti_version'] = 'LTI-1p0'
    context['lti_message_type'] = 'ContentItemSelection'
    context['data'] = request.POST['data']
    context['content_items'] = CONTENT_ITEM_TEMPLATE.format(
        submission_url,
        submission_url,
        title,
        description,
    )

    return render(request, 'inspector/return_homework_submission.html', context)


@csrf_exempt
@xframe_options_exempt
def view_assignment(request, assignment_id):
    launch_params = OrderedDict()
    for k in sorted(request.POST.dict().keys()):
        launch_params[k] = request.POST[k]
    return render(request, 'inspector/view_assignment.html', {'launch_params': launch_params, 'assignment_id': assignment_id})


@csrf_exempt
@xframe_options_exempt
def view_homework_submission(request, submission_id):
    launch_params = OrderedDict()
    for k in sorted(request.POST.dict().keys()):
        launch_params[k] = request.POST[k]

    content = lorem.text()

    return render(
        request,
        'inspector/view_submission.html',
        {'launch_params': launch_params, 'submission_id': submission_id, 'content': content}
    )
