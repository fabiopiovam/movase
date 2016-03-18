# -*- coding: utf-8 -*-

import urllib2, json, re

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import IntegrityError
from django.utils.html import strip_tags

from ia_client_api.models import Log, LogItem
from cms.models import Page
from tags import set_tags

class Command(BaseCommand):
    help = 'Importing Internet Archive contents of a Bookmarks'

    def handle(self, *args, **options):
        
        bookmars_url = 'http://archive.org/bookmarks/%s?output=json' % settings.IA_BOOKMARKS
        
        self.stdout.write(u'Requesting publications list of %s ...' % bookmars_url)
        
        publications, msg = self._get_json(bookmars_url)
        
        if (not publications):
            self.stdout.write(msg)
            log = Log(url=bookmars_url, message=msg)
            log.save()
            return 
        
        log = Log(url=bookmars_url, message='')
        log.save()
        
        total, imported, errors = 0, 0, 0
        
        for item in publications:
            
            self.stdout.write(u'Data request of %s ...' % item['identifier'])
            total += 1
            
            item_content, msg = self._get_json('http://archive.org/details/%s/?output=json' % item['identifier'])
            if (not item_content):
                self.stdout.write(msg)
                log_item = LogItem(log=log,
                                   identifier=item['identifier'],
                                   title=item['title'],
                                   imported=False,
                                   message=msg)
                log_item.save()
                errors += 1
                continue 

            #mount content
            files = {'photos':[],'audios':[],'videos':[]}
            
            for filename in item_content['files']:
                
                file                = item_content['files'][filename]
                file['filename']    = filename
                file['host']        = 'https://archive.org/download/%s/' % item['identifier']
                file['identifier']            = item['identifier']
                
                if (self._is_image(filename)):
                    f = self._add_photo(file)
                    if(f) : files['photos'].append(f)
                
                if (self._is_audio_derivative(file)):
                    file['original_details'] = item_content['files']['/' + file['original']]
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
            
            published_at = item_content['metadata']['publicdate'][0]
            summary = self._mount_summary(item_content)

            #persist page
            try:
                page = Page.objects.create(title=item_content['metadata']['title'][0],
                                           slug=item['identifier'], 
                                           summary=summary,
                                           content=content,
                                           published=True,
                                           published_at=published_at)
            except IntegrityError as e:
                total -= 1
                self.stdout.write('Warning: Page %s already exists!' % item['identifier'])
                continue
            except Exception as e:
                self.stdout.write(e.message)
                log_item = LogItem(log=log,
                                   identifier=item['identifier'],
                                   title=item['title'],
                                   imported=False,
                                   message=e.message)
                log_item.save()
                errors +=1
                continue

            set_tags(page, ','.join(item_content['metadata']['subject']))
            
            msg = u'Import success!'
            log_item = LogItem(log=log,
                               identifier=item['identifier'],
                               title=item['title'],
                               imported=True,
                               message=msg)
            log_item.save()
            imported += 1
            self.stdout.write(msg)
        
        log.total       = total
        log.imported    = imported
        log.errors      = errors
        log.save()
        
        self.stdout.write(u'Import finished!')
    
    
    def _mount_summary(self, item_content):
        
        summary = strip_tags(item_content['metadata']['description'][0])
        summary = summary[:350] + '...' if (len(summary) >= 350) else summary
        if (item_content['misc']['image']):
            summary = '<img src="%s" align="right" class="ia-summary-img" />%s' % (item_content['misc']['image'], summary)
        
        return summary
    
    
    def _mount_content(self, files):
        _return = files
        if (_return['photos']):
            _return['photos'] = '<div class="ia-image-gallery"><div>' + '</div><div>'.join(_return['photos']) + '</div></div>'
        
        if (_return['audios']):
            _return['audios'] = '<div class="ia-audio-gallery"><div>' + '</div><div>'.join(_return['audios']) + '</div></div>'
        
        return _return
    
    
    def _is_audio_derivative(self, file):
        regex = re.search(u'(mp3|ogg)$', file['filename'], re.IGNORECASE)
        return (regex and file['source'] == 'derivative')
    
    
    def _is_image(self, filename):
        return re.search(u'(jpeg|jpg|gif|png)$', filename, re.IGNORECASE)
    
    
    def _add_photo(self, file):
        if (file['source'] == 'original' or (not self._is_image(file['original']))):
            return ''
        
        href    = file['host'] + file['original']
        src     = file['host'] + file['filename']
        return '<a href="%s" data-lightbox="%s"><img src="%s"></a>' % (href, file['identifier'], src)
    
    
    def _add_audio(self, file):
        
        title   = file['original_details']['title'] if file['original_details'].has_key('title') else file['original']
        title   = title[:50] + '...' if (len(title)>=50) else title
        
        embed   = u'<iframe frameborder="0" src="https://archive.org/embed/%s/%s">Please upgrade your browser</iframe>' % (file['identifier'], file['original'])
        a_title = u"Clique com o botão direito e escolha 'Salvar link como...'"
        dl_mp3  = u'<a title="%s" target="_blank" href="https://archive.org/download/%s/%s">VBR MP3 (%s)</a>' % (a_title, file['identifier'], file['original'], file['original_details']['size'])
        dl_ogg  = u'<a title="%s" target="_blank" href="https://archive.org/download/%s/%s">Ogg Vorbis (%s)</a>' % (a_title, file['identifier'], file['filename'], file['size'])
        
        return u'%s <br /> %s <br /> %s | %s' % (title, embed, dl_mp3, dl_ogg)
    
    
    def _add_video(self, file):
        pass
    
    
    def _get_json(self, url):
        
        msg_404 = u'URL NotFound %s' % url
        msg_err = u'Erro to read %s' % url
        
        request = urllib2.Request(url)
        
        try:
            urlopen = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            
            if e.code == 404:
                msg = msg_404
            else:
                msg = msg_err
        except urllib2.URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            msg = msg_404
        else:
            # 200
            msg = u'imported!'
            content = urlopen.read()
        
            return json.loads(content), msg
        
        return False, msg