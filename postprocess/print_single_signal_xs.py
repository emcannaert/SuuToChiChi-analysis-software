import argparse
import sys,os

from return_signal_SF.return_signal_SF import return_signal_SF

if __name__=="__main__":

	parser = argparse.ArgumentParser(description="Return the Suu->chi chi->jets cross section.")
	parser.add_argument("--year", type=str, required=True, help="Input year on which to use.")
	parser.add_argument("--mass_point", type=str, required=True, help="The signal mass point to use.")
	parser.add_argument("--decay", type=str, required=True,  help="Signal decay to use.")
	parser.add_argument("--y_uu", type=float, required=False,  default= 2.0,  help="The y_uu coupling to use.")
	parser.add_argument("--y_x", type=float, required=False,   default= 2.0,  help="The y_x coupling to use.")
	parser.add_argument("--WB_BR", type=float, required=False, default= 0.5,  help="The WB branching fraction to use.")
	parser.add_argument("--ZT_BR", type=float, required=False, default= 0.25, help="The HT branching fraction to use.")
	parser.add_argument("--HT_BR", type=float, required=False, default= 0.25, help="The ZT branching fraction to use.")

	args = parser.parse_args()

	#print("year = %s, mass point = %s, decay = %s, y_uu = %s, y_x = %s, WB_BR = %s, ZT_BR = %s, HT_BR = %s."%(
	#	args.year,args.mass_point,args.decay, args.y_uu, args.y_x, args.WB_BR, args.ZT_BR, args.HT_BR
	#	))

	print(return_signal_SF(args.year,args.mass_point,args.decay, y_uu = args.y_uu, y_x = args.y_x, WB_BR = args.WB_BR, ZT_BR = args.HT_BR, HT_BR = args.ZT_BR))