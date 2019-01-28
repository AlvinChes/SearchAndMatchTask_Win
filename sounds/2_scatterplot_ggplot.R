###################################################################

setwd("~/Desktop/GraphsTablesJS")

library(foreign)
# library(sjPlot)
library(sjmisc)
library(dplyr)
library(ggplot2)

###################################################################
# (1) DATA PREPARATION
###################################################################

# load neuropsychological data file
demo_neuropsych = read.spss("neuropsychologie_1.sav", to.data.frame = TRUE, header = TRUE)
head(demo_neuropsych)

df_corr = demo_neuropsych %>%
  select("Probands",
         "frontalmc49_parietal_operculum80",
         "frontalmc49_smg_39", 
         "Frontalmc49_smg_37",
         "Frontalmc49_salience_150",
         "Frontalmc49_dorsal_attention_154", 
         "default_135_salience_150", 
         "default_135_cerebellum_108", 
         "parahippo64_3", 
         "parahippo64_37", 
         "parahippo64_68", 
         "parahippo64_78",
         "parahippo64_80",
         "parahippo64_138", 
         "parahippo64_146", 
         "TONI_IQ",
         "DurchstreichtestWP",
         "VerarbeitungsgeschwindigkeitIQ", 
         "EF_composite_neu",
         "Dauer_Therapieende", 
         "Composite_Atlantis",
         "AgeatDiagnosis",
         "FamilyAffluenceScale",
         "age",
         "dauer_Treatment") 

# rename brain regions -> http://www.thehumanbrain.info/database/nomenclature.php
df_corr = df_corr %>%
  rename("FMC-Op" = "frontalmc49_parietal_operculum80",
         "FMC-SMGp" = "frontalmc49_smg_39",
         "FMC-SMGa" = "Frontalmc49_smg_37",
         "FMC-SMG (SN)" = "Frontalmc49_salience_150",
         "FMC-dIPS (AN)" = "Frontalmc49_dorsal_attention_154",
         "SMGr (DMN, SN)" = "default_135_salience_150",
         "Cb (DMN)" = "default_135_cerebellum_108",
         "PHG-IG" = "parahippo64_3",
         "PHG-SMG" = "parahippo64_37",
         "PHG-FuG" = "parahippo64_68",
         "PHG-Op" = "parahippo64_78",
         "PHG-POp" = "parahippo64_80",
         "PHG-SMN" = "parahippo64_138",
         "PHG-IG (SN)" = "parahippo64_146",
         "IQ" = "TONI_IQ",
         "Attention" = "DurchstreichtestWP",
         "PS" = "VerarbeitungsgeschwindigkeitIQ",
         "EF" = "EF_composite_neu",
         "TST" = "Dauer_Therapieende",
         "VL" = "Composite_Atlantis",
         "AaD" = "AgeatDiagnosis",
         "SES" = "FamilyAffluenceScale",
         "Age" = "age",
         "TD" = "dauer_Treatment",
         "Group" = "Probands")

df_nonrecode = df_corr

# # recode 0 = 'controls' / 1 = 'patients' in "Probands" column
df_corr$Group[df_corr$Group == 0] = 'Controls'
df_corr$Group[df_corr$Group == 1] = 'CNS-'
df_corr

df_corr$Group = as.factor(df_corr$Group)

###################################################################
# (3) SCATTER PLOT
###################################################################

# plot IQ vs Cerebellum DMN

ggplot(df_corr, aes(x = IQ, y = `Cb (DMN)`, color=Group)) +
  geom_point() + 
  geom_smooth(method=lm, aes(fill=Group)) +
  labs(title="",
       x='Intellectual Function (IQ)', 
       y = 'Cerebellum (Default Mode Network)') +
  ylim(low = -1 , high = 1) + 
  theme_classic()  
    
# # plot IQ vs Cerebellum DMN
sjp.scatter(x = df_corr$IQ, y = df_corr$`Cb (DMN)`, grp = df_corr$Group,
            title = "",
            dot.labels = NULL,
            axis.titles = c('Intellectual Function (IQ)', 'Cerebellum (Default Mode Network)'),
            wrap.title = 50, wrap.legend.title = 20, wrap.legend.labels = 20,
            geom.size = 1, label.size = 3,
            show.axis.values = TRUE,
            fit.line.grps = TRUE, fit.line = FALSE, show.ci = TRUE, fitmethod = "lm")

# # plot PS vs FMC-SMGp

ggplot(df_corr, aes(x = PS, y = `FMC-SMGp`, color=Group)) +
  geom_point() + 
  geom_smooth(method=lm, aes(fill=Group)) +
  labs(title="",
       x='Processing Speed', 
       y = 'FMC-SMGp') +
  ylim(low = -1.5 , high = 1.5) + 
  theme_classic()

sjp.scatter(x = df_corr$PS, y = df_corr$`FMC-SMGp`, grp = df_corr$Group,
            title = "",
            legend.title = "Group", dot.labels = NULL,
            axis.titles = c('Processing Speed', 'FMC-SMGp'),
            wrap.title = 50, wrap.legend.title = 20, wrap.legend.labels = 20,
            geom.size = 1, label.size = 3,
            show.axis.values = TRUE,
            fit.line.grps = TRUE, fit.line = FALSE, show.ci = TRUE, fitmethod = "lm")
 
# # Processing speeed vs PHG-FuG

ggplot(df_corr, aes(x = PS, y = `PHG-FuG`, color=Group)) +
  geom_point() + 
  geom_smooth(method=lm, aes(fill=Group)) +
  labs(title="",
       x='Processing Speed', 
       y = 'PHG-FuG') +
  ylim(low = -1.5 , high = 1.5) + 
  theme_classic()
 
sjp.scatter(x = df_corr$PS, y = df_corr$`PHG-FuG`, grp = df_corr$Group,
            title = "",
            legend.title = "Group", dot.labels = NULL,
            axis.titles = c('Processing Speed', 'PHG-FuG'),
            wrap.title = 50, wrap.legend.title = 20, wrap.legend.labels = 20,
            geom.size = 1, label.size = 3,
            show.axis.values = TRUE,
            fit.line.grps = TRUE, fit.line = FALSE, show.ci = TRUE, fitmethod = "lm")
 
# # PHG-POp vs TST

ggplot(df_corr, aes(x = TST, y = `PHG-POp`, color=Group)) +
  geom_point() + 
  geom_smooth(method=lm, aes(fill=Group)) +
  labs(title="",
       x='Time since treatment', 
       y = 'PHG-POp') +
  ylim(low = -1.5 , high = 1.5) + 
  theme_classic()

sjp.scatter(x = df_corr$TST, y = df_corr$`PHG-POp`, grp = df_corr$Group,
            title = "",
            legend.title = "Group",
            dot.labels = NULL,
            axis.titles = c('Time since treatment', 'PHG-POp'),
            wrap.title = 50, wrap.legend.title = 20, wrap.legend.labels = 20,
            geom.size = 1, label.size = 3,
            show.axis.values = TRUE,
            fit.line.grps = TRUE, fit.line = FALSE, show.ci = TRUE, fitmethod = "lm")

# # PHG-POp vs VL

ggplot(df_corr, aes(x = VL, y = `PHG-POp`, color=Group)) +
  geom_point() + 
  geom_smooth(method=lm, aes(fill=Group)) +
  labs(title="",
       x='Verbal learning', 
       y = 'PHG-POp') +
  ylim(low = -1.5 , high = 1.5) + 
  theme_classic()

sjp.scatter(x = df_corr$VL, y = df_corr$`PHG-Op`, grp = df_corr$Group,
            title = "",
            legend.title = "Group",
            dot.labels = NULL,
            axis.titles = c('Verbal learning', 'PHG-POp'),
            wrap.title = 50, wrap.legend.title = 20, wrap.legend.labels = 20,
            geom.size = 1, label.size = 3,
            show.axis.values = TRUE,
            fit.line.grps = TRUE, fit.line = FALSE, show.ci = TRUE, fitmethod = "lm")

ggplot(df_corr, aes(x = AaD, y = `PHG-POp`, color=Group)) +
  geom_point() + 
  geom_smooth(method=lm, aes(fill=Group)) +
  labs(title="",
       x='Age at Diagnosis', 
       y = 'PHG-POp') +
  ylim(low = -1.5 , high = 1.5) + 
  theme_classic()
 
sjp.scatter(x = df_corr$AaD, y = df_corr$`PHG-Op`, grp = df_corr$Group,
            title = "",
            legend.title = "Group",
            dot.labels = NULL,
            axis.titles = c('Age at Diagnosis', 'PHG-POp'),
            wrap.title = 50, wrap.legend.title = 20, wrap.legend.labels = 20,
            geom.size = 1, label.size = 3,
            show.axis.values = TRUE,
            fit.line.grps = TRUE, fit.line = FALSE, show.ci = TRUE, fitmethod = "lm")

ggplot(df_corr, aes(x = Age, y = `PHG-POp`, color=Group)) +
  geom_point() + 
  geom_smooth(method=lm, aes(fill=Group)) +
  labs(title="",
       x='Age', 
       y = 'PHG-POp') +
  ylim(low = -1.5 , high = 1.5) + 
  theme_classic()

sjp.scatter(x = df_corr$Age, y = df_corr$`PHG-Op`, grp = df_corr$Group,
            title = "",
            legend.title = "Group",
            dot.labels = NULL,
            axis.titles = c('Age', 'PHG-POp'),
            wrap.title = 50, wrap.legend.title = 20, wrap.legend.labels = 20,
            geom.size = 1, label.size = 3,
            fit.line.grps = TRUE, fit.line = FALSE, show.ci = TRUE, fitmethod = "lm")
