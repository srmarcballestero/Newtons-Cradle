fig = figure();
while radi <= radi_final

    nom_carpeta = "../Simulacions/Gaps"+string(radi)+"dmm/Envelopes/";
    nom_out = nom_carpeta + "Gaps_"+nom_sim+"_"+string(radi)+"dmm_Fit_PosGap";
    disp("Accedint al directori"+nom_carpeta);

    gap_first = [];

    for i = 0:9
        for j = 0:9

            nom_inp_ini = nom_carpeta+"Gaps_"+string(i)+"_"+string(j)+"_"+nom_sim+"_"+string(radi)+"dmm_Ext_1_UpMax.csv";
            nom_inp_maxs = nom_carpeta+"Gaps_"+string(i)+"_"+string(j)+"_"+nom_sim+"_"+string(radi)+"dmm_Ext_2_UpMax.csv";

            str_gap = string(i)+"."+string(j);
            gap = double(str_gap);

            d1 = dir(nom_inp_ini);
            d2 = dir(nom_inp_maxs);

            if isempty(d1) || isempty(d2)
                continue;
            end

            disp("Llegint l'arxiu "+nom_inp_ini);
            disp("Llegint l'arxiu "+nom_inp_maxs);

            d1 = dir(nom_inp_ini);
            d2 = dir(nom_inp_maxs);
            if d1.bytes==0 || d2.bytes==0
                continue;
            end

            mins = csvread(nom_inp_ini, 0, 0);
            maxs = csvread(nom_inp_maxs, 0, 0);

            gap_first = [gap_first;[gap, mins(1,1), maxs(1,2)]];
        end
    end

    gaps = gap_first(:,1);
    poss = gap_first(:,2);
    ints = gap_first(:,3);

    scatter(gaps, poss, [], ints, 'filled');

    saveas(fig, nom_out+".png");

    [xData, yData] = prepareCurveData(gaps, poss);

    ft = fittype( 'power2' );
    opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
    opts.Display = 'Off';

    [fitresult, gof] = fit( xData, yData, ft, opts );

    out = fopen(nom_out+".dat", "w");
    fprintf(out, "%e\n%e\n%e\n%e\n%e\n%e\n%e\n%e\n", fitresult.a, fitresult.b, fitresult.c, gof.sse, gof.rsquare, gof.dfe, gof.adjrsquare, gof.rmse);
    fclose(out);

    clf();

    radi = radi + radi_pas;
end
