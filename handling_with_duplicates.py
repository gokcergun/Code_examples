import pandas as pd

fbref = pd.read_csv("fbref.csv")

## player demographics -> player, nation, position, squad, comp, age (same in all tables)
# standard stats table -> Playing time: Min; Performance: Gls, Ast; Expected: All
# passing table -> Total: Cmp, Att, PrgDist; Long: Prog
# goal and shot creation table -> SCA: SCA; SCA Types: All, GCA: GCA; GCA Types: All
# defensive table -> Tackles: Tkl, TklW; Pressures: Press, Succ; Blocks: Blocks, Int, Clr, Err
# possession table -> Touches: Live; Dribbles: Att, #Pl; Carries: TotDist, PrgDist; Receiving: Targ, Rec

df_fbref = fbref[['player', 'nation', 'position', 'squad', 'comp', 'age', 'stats_playingtime_min', 'stats_performance_gls',
                      'stats_performance_ast', 'stats_expected_xg', 'stats_expected_npxg', 'stats_expected_xa',
                      'pass_total_cmp', 'pass_total_att', 'pass_total_prg_dist', 'pass_prog', 'goal_sca_sca',
                      'goal_scatypes_pass_live', 'goal_scatypes_pass_dead', 'goal_scatypes_drib', 'goal_scatypes_sh',
                      'goal_scatypes_fld', 'goal_scatypes_def', 'goal_gca_gca', 'goal_gcatypes_pass_live',
                      'goal_gcatypes_pass_dead', 'goal_gcatypes_drib', 'goal_gcatypes_sh', 'goal_gcatypes_fld',
                      'goal_gcatypes_def', 'goal_gcatypes_og', 'defens_tackles_tkl', 'defens_tackles_tklw',
                      'defens_pressures_press', 'defens_pressures_succ', 'defens_blocks_blocks', 'defens_int',
                      'defens_clr', 'defens_err', 'possess_touches_live', 'possess_dribbles_att', 'possess_dribbles_p1',
                      'possess_carries_tot_dist', 'possess_carries_prd_dist', 'possess_receiving_targ',
                      'possess_receiving_rec']]

# There are two kinds of duplicates
#1. True duplicates - Same player - played in two different teams in 2019/2020 saison - should be handled
#2. Different players with the same name - Ex. Sergio Alvarez - should be kept

# show true duplicates
print(df_fbref[df_fbref.duplicated(subset=['player', 'age'], keep=False)].iloc[:,:7])
columns = ['stats_playingtime_min', 'stats_performance_gls',
                      'stats_performance_ast', 'stats_expected_xg', 'stats_expected_npxg', 'stats_expected_xa',
                      'pass_total_cmp', 'pass_total_att', 'pass_total_prg_dist', 'pass_prog', 'goal_sca_sca',
                      'goal_scatypes_pass_live', 'goal_scatypes_pass_dead', 'goal_scatypes_drib', 'goal_scatypes_sh',
                      'goal_scatypes_fld', 'goal_scatypes_def', 'goal_gca_gca', 'goal_gcatypes_pass_live',
                      'goal_gcatypes_pass_dead', 'goal_gcatypes_drib', 'goal_gcatypes_sh', 'goal_gcatypes_fld',
                      'goal_gcatypes_def', 'goal_gcatypes_og', 'defens_tackles_tkl', 'defens_tackles_tklw',
                      'defens_pressures_press', 'defens_pressures_succ', 'defens_blocks_blocks', 'defens_int',
                      'defens_clr', 'defens_err', 'possess_touches_live', 'possess_dribbles_att', 'possess_dribbles_p1',
                      'possess_carries_tot_dist', 'possess_carries_prd_dist', 'possess_receiving_targ',
                      'possess_receiving_rec']

#Take a summation of performance statistics for duplicated rows (not duplicated rows will remain as they are)
grouped = df_fbref.groupby(by=['player', 'age'])
for i in columns:
    df_fbref[i] = round(grouped[i].transform('sum'), 3)

#check the values after summation
print(df_fbref[df_fbref.duplicated(subset=['player', 'age'], keep=False)].iloc[:,:7])

# After the summation of performance statistics, duplicate rows now differ in team name ('squad').
# Since team information is unrelevant for our analysis, it does not matter which team name will be kept.

# However, some duplicate rows differ in also league name ('comp'). We are going to use league information in our analysis.
# Taking these players into the league relevant analysis would be misleading.
# Therefore, the players who played in two different league during the season will be flag before drop the duplicates
# and later will not be used into the league relevant analysis.

# drop one of the duplicated rows for the players who played in the same league during the season.
df_fbref.drop_duplicates(subset=['player', 'age', 'comp'], keep='last', inplace=True)

# Now the duplicated rows are only the players who played in two different league.(48 player)
print(len(df_fbref[df_fbref.duplicated(subset=['player', 'age'], keep=False)].iloc[:,:7])/2)

# flag duplicated rows
df_fbref = df_fbref.assign(was_duplicate = lambda d: d.duplicated(subset=['player', 'age'], keep=False))

# drop one of the duplicated rows
df_fbref.drop_duplicates(subset=['player', 'age'], keep='last', inplace=True, )

#reset the index of new data frame
df_fbref = df_fbref.reset_index(drop=True)

# Show different players with the same name - Duplicates (2. cases) will be kept.
df_fbref[df_fbref.duplicated('player', keep=False)]

# Data cleaning step- remove "-" from the player name
df_fbref[('player')]=df_fbref[('player')].str.replace("-", " ")

# write Dataframe into csv file
df_fbref.to_csv("fbref_final.csv")