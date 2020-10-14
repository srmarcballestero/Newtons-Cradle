posicions = true;

inp_nom_directori = input("Directori de treball (fill de Newton's Cradle/Simulacions/)?\n", "s");
nom_directori = "/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/"+inp_nom_directori+"/";

disp("Accedint al directori"+nom_directori);

noms_metadata = dir(fullfile(nom_directori+"Metadata/", "*Sim.dat"));
nom_directori_rel = nom_directori+"CmRel/Rel/";

for iter_fitxer = 1:length(noms_metadata)
  disp("Llegint el fitxer: "+"Metadata/"+noms_metadata(iter_fitxer).name)
  fitxer_metadata = fopen(char(nom_directori+"Metadata/"+noms_metadata(iter_fitxer).name), "r");
  fitxer_data = char(nom_directori_rel+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', 'Tmax.csv'));
  metadata = get_metadata(fitxer_metadata);
  fclose(fitxer_metadata);
  
  data = csvread(fitxer_data, 0, 0);
   
  t = data(:,1);
  max = data(:,2);
  
  try
      [xData, yData] = prepareCurveData( t, max );

      ft = fittype( 'A*exp(-B*x)+C', 'independent', 'x', 'dependent', 'y' );
%       excludedPoints = (yData < 0.5) | (yData > 1);
      opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
      opts.Algorithm = 'Levenberg-Marquardt';
      opts.Display = 'Off';
%       opts.Exclude = excludedPoints;


      [fitresult, gof] = fit( xData, yData, ft, opts );

      fitxer_fit = fopen(char(nom_directori_rel+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', 'FitEnv.dat')), "w");
      fprintf(fitxer_fit, "%e\n%e\n%e\n", fitresult.A, fitresult.B, fitresult.C);
  catch FitError
      fitxer_fit = fopen(char(nom_directori_rel+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', 'FitEnv.dat')), "w");
      fprintf(fitxer_fit, "%s\n%s\n%s\n", 1, 1, 1);
  end

end