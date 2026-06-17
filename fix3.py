code = open('src/dashboard.py', 'r', encoding='utf-8').read()

# Fix emoji codes
code = code.replace('&#127760;', '🪐')
code = code.replace('&#127777;', '🌡')
code = code.replace('&#128197;', '📅')
code = code.replace('&#127758;', '🌍')
code = code.replace('&#128207;', '📏')

# Fix scroll button - replace the scroll cta div
old = '''html.Div(["Scroll to Explore", html.Div(className="arrow")], className="scroll-cta"),'''
new = '''html.Div([
            html.Button("Scroll to Explore", id="scroll-btn",
                style={"background":"rgba(0,229,255,0.1)","border":"1px solid rgba(0,229,255,0.4)",
                       "color":"#00e5ff","padding":"12px 32px","borderRadius":"50px","cursor":"pointer",
                       "fontSize":"0.9rem","letterSpacing":"2px","textTransform":"uppercase",
                       "fontFamily":"Inter,sans-serif","marginBottom":"12px",
                       "transition":"all 0.3s ease"}),
            html.Div(className="arrow"),
        ], className="scroll-cta"),
        dcc.Location(id="url", refresh=False),'''
code = code.replace(old, new)

# Add scroll JS to the index_string - inject before </script>
code = code.replace(
    '})();\n</script>',
    '''})();
document.addEventListener('DOMContentLoaded', function(){
  var btn = document.getElementById('scroll-btn');
  if(btn){
    btn.addEventListener('click', function(){
      document.getElementById('dashboard').scrollIntoView({behavior:'smooth'});
    });
    btn.addEventListener('mouseover', function(){ this.style.background='rgba(0,229,255,0.2)'; this.style.boxShadow='0 0 20px rgba(0,229,255,0.3)'; });
    btn.addEventListener('mouseout',  function(){ this.style.background='rgba(0,229,255,0.1)'; this.style.boxShadow='none'; });
  }
});
</script>'''
)

with open('src/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Fixed!')