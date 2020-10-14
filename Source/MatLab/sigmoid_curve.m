posicions = true;

inp_nom_directori = input("Directori de treball (fill de Newton's Cradle/Simulacions/)?\n", "s");
nom_directori = "/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/"+inp_nom_directori+"/";

disp("Accedint al directori"+nom_directori);

noms_metadata = dir(fullfile(nom_directori+"Metadata/", "*Sim.dat"));
nom_directori_rel = nom_directori+"CmRel/Rel/";

for iter_fitxer = 1:length(noms_metadata)
  disp("Llegint el fitxer: "+"Metadata/"+noms_metadata(iter_fitxer).name)
  fitxer_metadata = fopen(char(nom_directori+"Metadata/"+noms_metadata(iter_fitxer).name), "r");
  fitxer_data = char(nom_directori_rel+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', 'Tdiff.csv'));
  metadata = get_metadata(fitxer_metadata);
  fclose(fitxer_metadata);
  
  data = csvread(fitxer_data, 0, 0);
   
  t = data(:,1);
  tau = data(:,2);
  
  try
      [xData, yData] = prepareCurveData( t, tau );

      ft = fittype( '0.5+0.5/(1+Q*exp(-D*x))^(1/v)', 'independent', 'x', 'dependent', 'y' );
      excludedPoints = (yData < 0.5) | (yData > 1);
      opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
      opts.Algorithm = 'Levenberg-Marquardt';
      opts.Display = 'Off';
      opts.Exclude = excludedPoints;


      [fitresult, gof] = fit( xData, yData, ft, opts );

      fitxer_fit = fopen(char(nom_directori_rel+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', 'FitFreq.dat')), "w");
      fprintf(fitxer_fit, "%e\n%e\n%e\n", fitresult.Q, fitresult.D, fitresult.v);
  catch FitError
      fitxer_fit = fopen(char(nom_directori_rel+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', 'FitFreq.dat')), "w");
      fprintf(fitxer_fit, "%e\n%e\n%e\n", 1, 1, 1);
  end

end