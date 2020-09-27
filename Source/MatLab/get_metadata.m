function metadata = get_metadata(mtd_file)
    metadata.N = int8(sscanf(fgetl(mtd_file), "%d"));
    metadata.g = double(sscanf(fgetl(mtd_file), "%e"));
    metadata.L = double(sscanf(fgetl(mtd_file), "%e"));
    metadata.R = double(sscanf(fgetl(mtd_file), "%e"));
    metadata.gap = double(sscanf(fgetl(mtd_file), "%e"));
    metadata.eta = double(sscanf(fgetl(mtd_file), "%e"));
    metadata.gamma = double(sscanf(fgetl(mtd_file), "%e"));
    metadata.A = double(sscanf(fgetl(mtd_file), "%e"));
    metadata.m = double(sscanf(fgetl(mtd_file), "%e"));
    metadata.E = double(sscanf(fgetl(mtd_file), "%e"));
    metadata.j = double(sscanf(fgetl(mtd_file), "%e"));
    metadata.pas = double(sscanf(fgetl(mtd_file), "%e"));
    metadata.num_osc = double(sscanf(fgetl(mtd_file), "%e"));
    metadata.salt = int8(sscanf(fgetl(mtd_file), "%e"));
end
