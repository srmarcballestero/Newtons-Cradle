fig = figure();
posicions = true;

inp_nom_directori = input("Directori de treball (fill de Newton's Cradle/Simulacions/)?\n", "s");
nom_directori = "/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/"+inp_nom_directori+"/";

mkdir([char(nom_directori) 'Envelopes/']);

disp("Accedint al directori"+nom_directori);

noms_metadata = dir(fullfile(nom_directori+"Metadata/", "*Sim.dat"));

for iter_fitxer = 1:length(noms_data)
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

  csvwrite(nom_directori+"Envelopes/"+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', 'Env.csv'), [env1up,env1lo,env2up,env2lo]);
  hold on;
    plot(env1up(:,1),env1up(:,2), 'blue');
    plot(env1lo(:,1),env1lo(:,2), 'blue');
    plot(env2up(:,1),env2up(:,2), 'red');
    plot(env2lo(:,1),env2lo(:,2), 'red');
    if posicions
        plot(pos1(:,1), pos1(:,2), 'cyan');
        plot(pos2(:,1), pos2(:,2), 'magenta');
    end
  hold off;
  saveas(fig, nom_directori+"Envelopes/"+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', 'Env.png'));
  clf();
end
