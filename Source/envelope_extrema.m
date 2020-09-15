
radi_inicial = input("Radi inicial (e-1 mm) ?");
radi_final = input("Radi final (e-1 mm) ?");
radi_pas = input("Pas dels radis (e-1 mm) ?");

nom_sim = input("Nom de les simulacions?", 's');

radi = radi_inicial;

while radi <= radi_final
    
    nom_carpeta = "../Simulacions/Gaps"+string(radi)+"dmm/Envelopes/";
    disp("Accedint al directori"+nom_carpeta);
    
    for i = 0:9
        for j = 0:9
            str_gap = string(i)+"."+string(j);
            chr_gap = convertStringsToChars(str_gap);
            nom_inp = nom_carpeta+"Gaps_"+string(i)+"_"+string(j)+"_"+nom_sim+"_"+string(radi)+"dmm_Env.csv";
            nom_out = nom_carpeta+"Gaps_"+string(i)+"_"+string(j)+"_"+nom_sim+"_"+string(radi)+"dmm_Ext_";

            d = dir(nom_inp);

            if isempty(d)
                continue;
            end

            disp("Llegint l'arxiu "+nom_inp);

            data = csvread(nom_inp, 0, 0);

            env1up = [data(:,1),data(:,2)];
            env1lo = [data(:,3),data(:,4)];
            env2up = [data(:,5),data(:,6)];
            env2lo = [data(:,7),data(:,8)];

            max1lo = islocalmax(env1lo(:,2));
            min1lo = islocalmin(env1lo(:,2));
            max1up = islocalmax(env1up(:,2));
            min1up = islocalmin(env1up(:,2));

            max2lo = islocalmax(env2lo(:,2));
            min2lo = islocalmin(env2lo(:,2));
            max2up = islocalmax(env2up(:,2));
            min2up = islocalmin(env2up(:,2));

            env1loX = env1lo(:,1);
            env1loY = env1lo(:,2);
            env1upX = env1up(:,1);
            env1upY = env1up(:,2);

            env2loX = env2lo(:,1);
            env2loY = env2lo(:,2);
            env2upX = env2up(:,1);
            env2upY = env2up(:,2);


            csvwrite(nom_out+"1_LoMax.csv", [env1loX(max1lo), env1loY(max1lo)]);
            csvwrite(nom_out+"1_LoMin.csv", [env1loX(min1lo), env1loY(min1lo)]);
            csvwrite(nom_out+"1_UpMax.csv", [env1upX(max1up), env1loY(max1up)]);
            csvwrite(nom_out+"1_UpMin.csv", [env1upX(min1up), env1loY(min1up)]);

            csvwrite(nom_out+"2_LoMax.csv", [env2loX(max2lo), env2loY(max2lo)]);
            csvwrite(nom_out+"2_LoMin.csv", [env2loX(min2lo), env2loY(min2lo)]);
            csvwrite(nom_out+"2_UpMax.csv", [env2upX(max2up), env2upY(max2up)]);
            csvwrite(nom_out+"2_UpMin.csv", [env2upX(min2up), env2upY(min2up)]);

    %         hold on;
    %         plot(env1up(:,1),env1up(:,2));
    %         plot(env1lo(:,1),env1lo(:,2));
    %         plot(env2up(:,1),env2up(:,2));
    %         plot(env2lo(:,1),env2lo(:,2));
    %         
    %         plot(env1loX(max1lo),env1loY(max1lo), 'r*');
    %         plot(env1loX(min1lo),env1loY(min1lo), 'r*');
    %         plot(env1upX(max1up),env1upY(max1up), 'g*');
    %         plot(env1upX(min1up),env1upY(min1up), 'g*');
    %         
    %         plot(env2loX(max2lo),env2loY(max2lo), 'g*');
    %         plot(env2loX(min2lo),env2loY(min2lo), 'g*');
    %         plot(env2upX(max2up),env2upY(max2up), 'r*');
    %         plot(env2upX(min2up),env2upY(min2up), 'r*');
    %         
    %         
    %         hold off;
    %         input("");
    %         clf();

        end
    end
    radi = radi + radi_pas;
end
