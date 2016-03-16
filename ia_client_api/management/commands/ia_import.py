# -*- coding: utf-8 -*-

import urllib2, json, re

from django.core.management.base import BaseCommand, CommandError

from ia_client_api.models import Imports, ImportItems
from cms.models import Page
from tags import set_tags

class Command(BaseCommand):
    help = 'Importing Internet Archive contents of a Bookmarks'

    def handle(self, *args, **options):
    
        publications = self._get_json('http://archive.org/bookmarks/Radio%20da%20Juventude?output=json')
        
        for item in publications:
            
            self.stdout.write(u'Requisitando dados de %s ...' % item['identifier'])
            
            item_content = self._get_json('http://archive.org/details/%s/?output=json' % item['identifier'])
            
            #mount content
            files = {'photos':[],'audios':[],'videos':[]}
            
            for filename in item_content['files']:
                
                file                = item_content['files'][filename]
                file['filename']    = filename
                file['host']        = 'https://archive.org/download/%s/' % item['identifier']
                
                if (self._is_image(filename)):
                    f = self._add_photo(file)
                    if(f) : files['photos'].append(f)
                
                if (re.search(u'(mp3|ogg)$', filename, re.IGNORECASE)):
                    f = self._add_audio(file)
                    if(f) : files['audios'].append(f)
                
                if (re.search(u'(mp4)$', filename, re.IGNORECASE)):
                    f = self._add_video(file)
                    if(f) : files['videos'].append(f)
            
            media_content = self._mount_content(files)
            content = item_content['metadata']['description'][0]
            content += media_content['videos'] if media_content['videos'] else ''
            content += media_content['audios'] if media_content['audios'] else ''
            content += media_content['photos'] if media_content['photos'] else ''
            
            #persist page
            page = Page(title=item_content['metadata']['title'][0], 
                 slug=item['identifier'], 
                 content=content,
                 published=True)
            page.save()
            set_tags(page, ','.join(item_content['metadata']['subject']))
            
            self.stdout.write(u'Importado com sucesso!')
        
        self.stdout.write(u'Importação concluída com sucesso!')
    
    def _mount_content(self, files):
        _return = files
        if (_return['photos']):
            _return['photos'] = '<div class="ia-image-gallery"><div>' + '</div><div>'.join(_return['photos']) + '</div></div>'
        
        return _return
        
    def _is_image(self, filename):
        return re.search(u'(jpeg|jpg|gif|png)$', filename, re.IGNORECASE)
    
    def _add_photo(self, file):
        if (file['source'] == 'original' or (not self._is_image(file['original']))):
            return ''
        
        href    = file['host'] + file['original']
        src     = file['host'] + file['filename']
        return '<a href="%s"><img src="%s"></a>' % (href, src)
    
    def _add_audio(self, file):
        pass
        
    def _add_video(self, file):
        pass
    
    def _get_json(self, url):
        request = urllib2.Request(url)
        urlopen = urllib2.urlopen(request)
        content = urlopen.read()
        
        return json.loads(content)