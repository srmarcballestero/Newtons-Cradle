fig = figure();
posicions = true;

radi_inicial = input("Radi inicial (e-1 mm) ?");
radi_final = input("Radi final (e-1 mm) ?");
radi_pas = input("Pas dels radis (e-1 mm) ?");

nom_sim = input("Nom de les simulacions?", 's');

radi = radi_inicial;

while radi <= radi_final
    
    nom_carpeta = "../Simulacions/Gaps"+string(radi)+"dmm/";
    
    mkdir([char(nom_carpeta) 'Envelopes/']);
    
    disp("Accedint al directori"+nom_carpeta);
    
    for i = 0:9
        for j = 0:9
            str_gap = string(i)+"."+string(j);
            chr_gap = convertStringsToChars(str_gap);
            nom_inp = nom_carpeta + "Gaps_"+string(i)+"_"+string(j)+"_"+nom_sim+"_"+string(radi)+"dmm.csv";
            nom_out = "Gaps_"+string(i)+"_"+string(j)+"_"+nom_sim+"_"+string(radi)+"dmm_Env";;

            d = dir(nom_inp);

            if isempty(d)
                disp("No s'ha trobat el fitxer"+nom_inp);
                continue;
            end

            disp("Llegint l'arxiu "+nom_inp);

            data = csvread(nom_inp, 0, 0);
            pos1 = data(:,1:2);
            pos2 = [data(:,1), data(:,3)];

            [env1up, env1lo] = envelope(pos1, 400, 'peak');
            [env2up, env2lo] = envelope(pos2, 400, 'peak');

            csvwrite(nom_carpeta+"Envelopes/"+nom_out+".csv", [env1up,env1lo,env2up,env2lo]);


            hold on;
            plot(env1up(:,1),env1up(:,2), 'blue');
            plot(env1lo(:,1),env1lo(:,2), 'blue');
%             plot(env2up(:,1),env2up(:,2), 'red');
%             plot(env2lo(:,1),env2lo(:,2), 'red');
            if posicions
                plot(pos1(:,1), pos1(:,2), 'cyan');
%                 plot(pos2(:,1), pos2(:,2), 'magenta');
            end
            hold off;
            saveas(fig, nom_carpeta+"Envelopes/"+nom_out+".png");
            clf();
        end
    end
    
    radi = radi + radi_pas;
        
end

clf();
