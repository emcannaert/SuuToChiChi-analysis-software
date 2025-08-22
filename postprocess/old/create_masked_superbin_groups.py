import ast

def get_masked_groups(groups, mask):
    mask_sorted = sorted(mask)
    removed_so_far = 0

    for m in mask_sorted:
        effective = m - removed_so_far
        new_groups = []
        for g in groups:
            new_g = []
            for idx in g:
                if idx == effective:
                    # drop this bin
                    continue
                elif idx > effective:
                    new_g.append(idx - 1)
                else:
                    new_g.append(idx)
            if new_g:
                new_groups.append(new_g)
        groups = new_groups
        removed_so_far += 1
    return groups


if __name__=="__main__":
    superbin_groups_dir  = "superbinGroups/"
    region_mask_dir = "region_masks/"

    #### You likely do not want to use this  ----> want 1b/0b regions to use the same superbin maps, but NOT the same masks (which is what this does)

    use_1b_maps_for_0b = True    # means the SR+CR / AT1b+AT0b regions use the same maps (1b and 0b use the same) 

    mask_dict = {}
    groups_dict = {}

    years = ["2015","2016","2017","2018"]
    regions = ["SR","CR","AT1b","AT0b"]
    techniques = ["NN_",""] ## currently not needed 



    if use_1b_maps_for_0b: _1b_map_translator = {"SR":"SR","CR":"SR","AT1b":"AT1b","AT0b":"AT1b"}
    else: _1b_map_translator = {"SR":"SR","CR":"CR","AT1b":"AT1b","AT0b":"AT0b"}

    use_QCD_Pt_opts = [True,False]
    use_QCD_Pt_strs = ["QCDPT","QCDHT"]


    for use_QCD_Pt_str in use_QCD_Pt_strs:


        for year in years:
            mask_path  = region_mask_dir + "%s_bin_masks_%s.txt"%(use_QCD_Pt_str,year)
            group_path = superbin_groups_dir + "%s_superbin_groups_%s.txt"%(use_QCD_Pt_str,year)
            output_group_name = superbin_groups_dir + "masked/%s_superbin_groups_%s.txt"%(use_QCD_Pt_str,year)
            
            ## get masks 
            mask_dict[year] = {}
            for region in regions:
                mask_dict[year][region] = []


            with open(mask_path) as f:
                lines = f.readlines()
            for line in lines:
                _year,region,technique,mask = line.split("/")
                if "NN" in technique: continue # not dealing with this now
                mask = mask.strip()
                mask = ast.literal_eval(mask)
                mask_dict[_year][region] = mask


            ## get groups
            groups_dict[year] = {}
            for region in regions:
                groups_dict[year][region] = []

            with open(group_path) as f:
                lines = f.readlines()
            for line in lines:
                _year,region,desc,groups = line.split("/")
                #print("groups are %s"%groups)
                groups = ast.literal_eval(groups)
                groups_dict[year][region] = groups


            # write out masked groups 

            outfile = open(output_group_name,"w")

            for region in regions:
                region_to_use = _1b_map_translator[region]
                groups = groups_dict[_year][region_to_use]  # if use_1b_maps_for_0b, this will use SR/AT1b instead of CR/AT0b groups 

                masked_groups = get_masked_groups(groups, mask_dict[_year][ region] )
                new_n_groups = len(masked_groups)
                desc = "number of superbin groups =%d"%( new_n_groups)
                outfile.write("%s/%s/%s/%s\n" % (_year, region, desc, masked_groups))            

            
            outfile.close()
            print("Wrote masked superbinGroup text files to %s."%(superbin_groups_dir + "masked/"))
            """for line in lines:
                _year,region,desc,groups = line.split("/")

                desc_beg,_ = desc.split("=")
                groups = ast.literal_eval(groups)
                masked_groups = get_masked_groups(groups, mask_dict[_year][ _1b_map_translator[region]])

                new_n_groups = len(masked_groups)

                #print("%s/%s/%s = %s/%s\n"%(year,region, desc_beg,new_n_groups   ,masked_groups))
                outfile.write("%s/%s/%s=%d/%s\n" % (_year, region, desc_beg, new_n_groups, masked_groups))     """       
            






