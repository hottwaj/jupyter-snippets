# -*- coding: utf-8 -*-
"""
Created on Dec 01 2016

@author: jclarke
"""

from typing import Union

def init_notebook(default_figure_size = (6, 4), full_width: Union[float, bool] = True, default_figure_format = 'svg'):
    from IPython.core.display import display
    #run "magic" commands that you'd otherwise need to put into the cell as e.g. "%matplotlib inline"
    _ipy = get_ipython()
    _ipy.magic("matplotlib inline")
    
    #set default size for figures
    from pylab import rcParams
    rcParams['figure.figsize'] = default_figure_size

    #if default_figure_format == 'png':
    #    _ipy.magic("config InlineBackend.figure_format = 'retina'")
    #else:
    #    _ipy.magic("config InlineBackend.figure_format = '%s'" % default_figure_format)

    #use given format (svg, png, retina) for matplotlib graphics
    if default_figure_format: #if not given, assume its in config
        from IPython.core.display import HTML, set_matplotlib_formats
        set_matplotlib_formats(default_figure_format)
    
    #reduce size of IPython output cache which I never use (it defaults to 1000!)
    import IPython
    IPython.InteractiveShell.cache_size = 5

    #set default seaborn style
    import seaborn
    seaborn.set(style='whitegrid')
    #use a nice 6-colour palette that I had got used to. 
    #As of 2019-01-25 seaborn 0.9.0 introduced a new 10-colour palette - obvs this has more colours, but I prefer the ones in the old palette
    seaborn.set_palette("deep6")    

    #notebook layout modifications...
    from IPython.core.display import HTML
    if full_width:
        if full_width == True:
            nb_width = 1.0
        else:
            nb_width = full_width
        nb_width_css = ".container { width:%f%% !important; }" % (full_width*100)
    else:
        nb_width_css = ""
    display(HTML("""
    <style>
    %s
    div.widget-numeric-text {
      width: inherit !important;
    }
    .widget-label {
      min-width: inherit !important;
      max-width: none !important;
      width: 300px;
      padding-left: 8px;
    }
    #toc-wrapper {
      border: none !important;
    }

    div.run_this_cell { 
         display: none !important; 
    }
    
    #reduced width for text cells to avoid really long lines in text...
    .text_cell_render { 
        width: 60%% !important
    }
    </style>
    """ % nb_width_css))

def df_viewer(df, force_window_width = False, height = 400, *args, **kwargs):
    #this form of table is best for browsing very large tables
    
    grid_options = {'forceFitColumns': force_window_width, 'height': height}
    grid_options.update(kwargs.get('grid_options', {}))
    kwargs['grid_options'] = grid_options
    
    import qgrid
    return qgrid.show_grid(df, *args, **kwargs)

def show_hide_code_btn():
    from IPython.core.display import display, HTML, Javascript

    # This line will hide code by default when the notebook is exported as HTML
    display(Javascript('''
        var code_style_tag = null;
        function show_hide_code_toggle() {
            if (code_style_tag == null) {
                code_style_tag = addStyleString('.code_cell .input_area {display: none !important;} .prompt, .output_stderr {display: none !important;} .cell {padding: 0px !important;}');
            } else {
                code_style_tag.remove();
                code_style_tag = null
            }
            //jQuery('.code_cell .input_area').toggle(); 
            //jQuery('.prompt').toggle(); 
            //jQuery('.output_stderr').toggle(); 
            if (jQuery('.cell').css('padding') != '0px') {
                jQuery('.cell').css('padding', '0px');
            } else {
                jQuery('.cell').css('padding', '5px');
            }
        }
        
        function addStyleString(str) {
            var node = document.createElement('style');
            node.innerHTML = str;
            document.body.appendChild(node);
            return node;
        }       
        
        setTimeout(function() {
            if (window['IPython'] != undefined) {
                jQuery('.show_hide_code_btn').css('display', 'inline-block');
            } else {
                addStyleString('.simpletable {font-size: 16px}');
                addStyleString('.slides {zoom: 1.0 !important; width: 1200px !important; height: 900px !important; font-size: 16px !important}');
            }
        }, 1000);
            
        jQuery(function() {if (jQuery("body.notebook_app").length == 0) { show_hide_code_toggle(); }});'''))

    # This line will add a button to toggle visibility of code blocks, for use with the HTML export version
    display(HTML('''<button onclick="show_hide_code_toggle();" class="show_hide_code_btn" style="display: none">Show/hide code</button>'''))
