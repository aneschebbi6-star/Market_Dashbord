import importlib,inspect,sys
importlib.invalidate_caches()
import fetcher
print('MODULE_FILE:', fetcher.__file__)
print('HAS_get_news:', hasattr(fetcher,'get_news'))
print('EXPORTS:', [n for n in dir(fetcher) if n.startswith('get') or n.startswith('analyze') or n.endswith('news')][:200])
print('\n--- SOURCE TAIL ---\n')
src = open(fetcher.__file__, 'r', encoding='utf-8').read()
print('\n'.join(src.splitlines()[-120:]))
