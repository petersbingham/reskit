import reskit as rk

POLE_DATA_FOLDER = "create_formatted_QI_tables"

smatfit = rk.get_tool(rk.mcsmatfit, None)

typs = ["latex","html","raw"]
quants = ["E","k"]
truns = [True, False]
sig_digits = [None,4,10]

def _create_table(typ, quant, trun, sig_digit):
    smatfit.create_formatted_QI_tables(typ+quant, trun, sig_digit,
                                       spec_path=POLE_DATA_FOLDER)

for typ in typs:
    for quant in quants:
        for trun in truns:
            for sig_digit in sig_digits:
                _create_table(typ, quant, trun, sig_digit)
