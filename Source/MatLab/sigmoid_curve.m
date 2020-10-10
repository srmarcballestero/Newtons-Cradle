posicions = true;

inp_nom_directori = input("Directori de treball (fill de Newton's Cradle/Simulacions/)?\n", "s");
nom_directori = "/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/"+inp_nom_directori+"/";

disp("Accedint al directori"+nom_directori);

noms_metadata = dir(fullfile(nom_directori+"Metadata/", "*Sim.dat"));
nom_directori_rel = nom_directori+"CmRel/Rel/";

iter_fitxer = 80;
% for iter_fitxer = 1:length(noms_metadata)
  disp("Llegint el fitxer: "+"Metadata/"+noms_metadata(iter_fitxer).name)
  fitxer_metadata = fopen(char(nom_directori+"Metadata/"+noms_metadata(iter_fitxer).name), "r");
  fitxer_data = char(nom_directori_rel+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', 'Tdiff.csv'));
  metadata = get_metadata(fitxer_metadata);
  fclose(fitxer_metadata);
  
  data = csvread(fitxer_data, 0, 0);
   
  t = data(:,1);
  tau = data(:,2);
  
  input("");

% end