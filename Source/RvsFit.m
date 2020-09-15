radi_inicial = input("Radi inicial (e-1 mm) ?");
radi_final = input("Radi final (e-1 mm) ?");
radi_pas = input("Pas dels radis (e-1 mm) ?");

nom_sim = input("Nom de les simulacions?", 's');

radi = radi_inicial;

r = [];
a = [];
b = [];
c = [];

while radi <= radi_final
    
    nom_carpeta = "../Simulacions/Gaps"+string(radi)+"dmm/Envelopes/";
    nom_inp = nom_carpeta + "Gaps_"+nom_sim+"_"+string(radi)+"dmm_Fit_PosGap.dat";
    disp("Accedint al directori"+nom_carpeta);
    
    inp = fopen(nom_inp, "r");
    
    fitData = fscanf(inp, "%e");
    
    r = [r, radi * 1e-4];
    a = [a, fitData(1)];
    b = [b, fitData(2)];
    c = [c, fitData(3)];
    
    radi = radi + radi_pas;
end

scatter(r, b, [], c, 'filled');
