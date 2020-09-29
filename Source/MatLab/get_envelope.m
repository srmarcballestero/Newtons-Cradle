fig = figure();
posicions = true;

inp_nom_directori = input("Directori de treball (fill de Newton's Cradle/Simulacions/)?\n", "s");
nom_directori = "/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/"+inp_nom_directori+"/";

mkdir([char(nom_directori) 'Envelopes/']);

disp("Accedint al directori"+nom_directori);

noms_metadata = dir(fullfile(nom_directori+"Metadata/", "*Sim.dat"));


for iter_fitxer = 1:length(noms_metadata)
  disp("Llegint el fitxer: "+"Metadata/"+noms_metadata(iter_fitxer).name)
  disp("Llegint el fitxer: "+"Data/"+strrep(noms_metadata(iter_fitxer).name, ".dat", ".csv"))
  fitxer_metadata = fopen(char(nom_directori+"Metadata/"+noms_metadata(iter_fitxer).name), "r");
  fitxer_data = char(nom_directori+"Data/"+strrep(noms_metadata(iter_fitxer).name, '.dat', '.csv'));
  metadata = get_metadata(fitxer_metadata);
  fclose(fitxer_metadata);
  data = csvread(fitxer_data, 0, 0);

  pos1 = data(:,1:2);
  pos2 = [data(:,1), data(:,3)];

  [env1up, env1lo] = envelope(pos1, 400, 'peak');
  [env2up, env2lo] = envelope(pos2, 400, 'peak');

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

  csvwrite(nom_directori+"Envelopes/"+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', 'Env.csv'), [env1up,env1lo,env2up,env2lo]);

  csvwrite(nom_directori+"Envelopes/"+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', "Env_1_LoMax.csv"), [env1loX(max1lo), env1loY(max1lo)]);
  csvwrite(nom_directori+"Envelopes/"+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', "Env_1_LoMin.csv"), [env1loX(min1lo), env1loY(min1lo)]);
  csvwrite(nom_directori+"Envelopes/"+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', "Env_1_UpMax.csv"), [env1upX(max1up), env1loY(max1up)]);
  csvwrite(nom_directori+"Envelopes/"+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', "Env_1_UpMin.csv"), [env1upX(min1up), env1loY(min1up)]);

  csvwrite(nom_directori+"Envelopes/"+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', "Env_2_LoMax.csv"), [env2loX(max2lo), env2loY(max2lo)]);
  csvwrite(nom_directori+"Envelopes/"+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', "Env_2_LoMin.csv"), [env2loX(min2lo), env2loY(min2lo)]);
  csvwrite(nom_directori+"Envelopes/"+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', "Env_2_UpMax.csv"), [env2upX(max2up), env2upY(max2up)]);
  csvwrite(nom_directori+"Envelopes/"+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', "Env_2_UpMin.csv"), [env2upX(min2up), env2upY(min2up)]);

  hold on;
    plot(env1up(:,1),env1up(:,2), 'blue');
    plot(env1lo(:,1),env1lo(:,2), 'blue');
    plot(env2up(:,1),env2up(:,2), 'red');
    plot(env2lo(:,1),env2lo(:,2), 'red');

    plot(pos1(:,1), pos1(:,2), 'cyan');
    plot(pos2(:,1), pos2(:,2), 'magenta');

    plot(env1loX(max1lo),env1loY(max1lo), 'r*');
    plot(env1loX(min1lo),env1loY(min1lo), 'r*');
    plot(env1upX(max1up),env1upY(max1up), 'g*');
    plot(env1upX(min1up),env1upY(min1up), 'g*');

    plot(env2loX(max2lo),env2loY(max2lo), 'g*');
    plot(env2loX(min2lo),env2loY(min2lo), 'g*');
    plot(env2upX(max2up),env2upY(max2up), 'r*');
    plot(env2upX(min2up),env2upY(min2up), 'r*');
  hold off;

  saveas(fig, nom_directori+"Envelopes/"+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', 'Env.png'));
  clf();
end
close all;
