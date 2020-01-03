from dnslib import RR,QTYPE,TXT
from dnslib.server import DNSServer,DNSHandler,BaseResolver,DNSLogger

_ASSETS = {
	"abox":"Rory M",
	"anotherbox":"Rory M",
	"machine-name":"Another Guy",
}

class ZoneResolver(BaseResolver):
	def resolve(self,request,handler):
		reply = request.reply()
		reqname = str(request.q.qname)[:-1] # Strip the '.' from the end
		reqname = reqname.lower() # Lower case
		# print("Request for {}".format(reqname))
		if reqname in _ASSETS:
			reply.add_answer(RR("asset.owner",QTYPE.TXT,rdata=TXT(_ASSETS[reqname])))
		else:
			reply.add_answer(RR("asset.owner",QTYPE.TXT,rdata=TXT("Unknown")))
		return reply

if __name__ == '__main__':
	import argparse,time
	p = argparse.ArgumentParser(description="Zone DNS Resolver")
	p.add_argument("--port","-p",type=int,default=53,
						metavar="<port>",
						help="Server port (default:53)")
	p.add_argument("--address","-a",default="",
						metavar="<address>",
						help="Listen address (default:all)")
	p.add_argument("--glob",action='store_true',default=False,
						help="Glob match against zone file (default: false)")
	p.add_argument("--udplen","-u",type=int,default=0,
					metavar="<udplen>",
					help="Max UDP packet length (default:0)")
	p.add_argument("--tcp",action='store_true',default=False,
						help="TCP server (default: UDP only)")
	p.add_argument("--log",default="request,reply,truncated,error",
					help="Log hooks to enable (default: +request,+reply,+truncated,+error,-recv,-send,-data)")
	p.add_argument("--log-prefix",action='store_true',default=False,
					help="Log prefix (timestamp/handler/resolver) (default: False)")
	args = p.parse_args()
	
	resolver = ZoneResolver()
	logger = DNSLogger(args.log,args.log_prefix)

	# print("Starting Zone Resolver (%s:%d) [%s]" % (
	#					args.address or "*",
	#					args.port,
	#					"UDP/TCP" if args.tcp else "UDP"))

	if args.udplen:
		DNSHandler.udplen = args.udplen

	udp_server = DNSServer(resolver,
						   port=args.port,
						   address=args.address,
						   logger=logger)
	udp_server.start_thread()

	if args.tcp:
		tcp_server = DNSServer(resolver,
							   port=args.port,
							   address=args.address,
							   tcp=True,
							   logger=logger)
		tcp_server.start_thread()

	while udp_server.isAlive():
		time.sleep(1)
