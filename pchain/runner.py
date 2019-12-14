def run(filename,debugmode=False) :
  import pchain
  import sys
  
  Service = pchain.cleinit()
  SrvGroup = Service._ServiceGroup;

  pchain.IsRunFromPChain = True
  Result = Service._DoFile(modulename,filename,"")
  if Result[0] == False :
    print(Result[1])
    return False
  
  query = SrvGroup._NewQueryRecord()  
  hostobj = Service.PCRealmBase._FirstInst(query)
  Service.PCRealmBase._QueryClose(query) 
  if hostobj == None :
    print('PCRealmBase instance is not created')
    return False
    
  if debugmode == False :
    hostobj.Execute()
    SrvGroup._ClearService()
    libstarpy._ModuleExit()
    return True    
  
  libstarpy._SRPUnLock()
          
  from flask import Flask, Response, jsonify, request,send_file, send_from_directory
  import os


  app = Flask(__name__)

  @app.route('/realm/status', methods=['GET'])
  def status_tasks():
    libstarpy._SRPLock()
    hostobj.BreakOnProc(None)
    para = hostobj.GetStatusWithPos(None,0,0,0,0,0);
    Result = para._ToJSon()
    libstarpy._SRPUnLock()
    return Result
  
  @app.route('/realm/cellstatus/<string:object_id>', methods=['GET'])
  def cell_status_tasks(object_id):
    libstarpy._SRPLock()
    obj = Service._GetObject(object_id)
    if obj == None :
      libstarpy._SRPUnLock()
      return "",404
    hostobj.BreakOnProc(obj)
    para = hostobj.GetStatusWithPos(obj,0,0,0,0,0);
    Result = para._ToJSon()
    libstarpy._SRPUnLock()
    return Result  
    
  @app.route('/realm/runonce', methods=['GET'])
  def runonce_task():
    libstarpy._SRPLock()
    hostobj.BreakOnProc(None)
    hostobj.BreakOnProcContinue()
    para = hostobj.GetStatusWithPos(None,0,0,0,0,0);
    Result = para._ToJSon()
    libstarpy._SRPUnLock()
    return Result
  
  @app.route('/realm/cellrunonce/<string:object_id>', methods=['GET'])
  def cell_runonce_task(object_id):
    libstarpy._SRPLock()
    obj = Service._GetObject(object_id)
    if obj == None :
      libstarpy._SRPUnLock()
      return "",404  
    hostobj.BreakOnProc(obj)
    hostobj.BreakOnProcContinue()
    para = hostobj.GetStatusWithPos(obj,0,0,0,0,0);
    Result = para._ToJSon()
    libstarpy._SRPUnLock()
    return Result  

  def get_file(filename): 
    try:
        f = None
        if pchain.ispython2 == True :
          f = open(filename)
        else :
        	f = open(filename,encoding='utf-8')
        t = f.read()
        f.close()
        return t
    except IOError as exc:
        return str(exc)
        
  @app.route("/")
  def index_page():
    content = get_file(os.path.join(pchain.webpath,'index.html'))
    #return send_static_file(pchain.webpath,'index.html', as_attachment=True)
    return Response(content, mimetype="text/html")
    
  @app.route('/', defaults={'path': ''})
  @app.route('/<path:path>')
  def get_resource(path):
    mimetypes = {
      ".css": "text/css",
      ".html": "text/html",
      ".js": "application/javascript",
    }
    complete_path = os.path.join(pchain.webpath, path)
    ext = os.path.splitext(path)[1]
    mimetype = mimetypes.get(ext, "text/html")
    content = get_file(complete_path)
    return Response(content, mimetype=mimetype)
  
  '''  
  @app.route('/cle/<path:others>', methods=['GET'])
  def get_cle(others):
    code,res = Service._RestfulCall("/"+others,"get",request.json)
    if code != 200 :
      abort(code)
    return res 
  '''     
  
  print('using : http://localhost:4000')
  app.run(host="0.0.0.0", port=4000, debug=False)  

  libstarpy._SRPLock()
  hostobj.CancelBreakOnProc()

  SrvGroup._ClearService()
  libstarpy._ModuleExit()
  return True