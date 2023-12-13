import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods


class VisualizerView(TemplateView):
    template_name = 'visualizer/visualizer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = json.dumps(r[0])
            context['voting_results'] = {
                'labels': [opt['option'] for opt in r[0]['postproc']],
                'votes': [opt['votes'] for opt in r[0]['postproc']],
            }

            if r[0]['postproc']:
                max_option = max(r[0]['postproc'], key=lambda x: x['votes'])
                context['max_votes_option'] = max_option['option']
        except:
            raise Http404

        return context