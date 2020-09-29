inp_nom_directori = input("Directori de treball (fill de Newton's Cradle/Simulacions/)?\n", "s");
nom_directori = "/home/marc/OneDrive/Documents/Universitat/Física/S4 - Mecànica/Newton's Cradle/Simulacions/"+inp_nom_directori+"/";


disp("Accedint al directori"+nom_directori);

noms_metadata = dir(fullfile(nom_directori+"Metadata/", "*Sim.dat"));
nom_envelopes = nom_directori+"Envelopes/";

gammes = [];
temps = [];
ints = [];

for iter_fitxer = 1:length(noms_metadata)
  disp("Llegint el fitxer: "+"Metadata/"+noms_metadata(iter_fitxer).name);
  fitxer_metadata = fopen(char(nom_directori+"Metadata/"+noms_metadata(iter_fitxer).name), "r");
  metadata = get_metadata(fitxer_metadata);
  gammes = [gammes, metadata.gamma];
  fclose(fitxer_metadata);

  fitxer_maxs = char(nom_directori+"Envelopes/"+strrep(noms_metadata(iter_fitxer).name, 'Sim.dat', 'Env_1_UpMax.csv'));
  data_maxs = csvread(fitxer_maxs);

  ints = [ints, data_maxs(1, 2)];
  temps = [temps, data_maxs(1, 1)];


  scatter(gammes, temps, [], ints, 'filled');


%   [xData, yData] = prepareCurveData(gammes, temps);
%
%   ft = fittype( 'power1' );
%   opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
%   opts.Display = 'Off';
%
%   [fitresult, gof] = fit( xData, yData, ft, opts);
%
%   out = fopen(nom_out+".dat", "w");
%   fprintf(out, "%e\n%e\n%e\n%e\n%e\n%e\n%e\n", fitresult.a, fitresult.b, gof.sse, gof.rsquare, gof.dfe, gof.adjrsquare, gof.rmse);
%   fclose(out);

  clf();

end
