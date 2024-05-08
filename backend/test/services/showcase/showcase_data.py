import pytest

from sqlalchemy.orm import Session
from ....models.showcase_project import *

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

# Do not try this at home.

DATA = """A1,Deysi Morales-Magadan,Luis Rivera Gonzalez,Bailey Van Wormer,Sajan Patel, ,Other: CSXL Lost and Found,https://youtu.be/Hp3kcNHN-Bw,https://final-team-a1-comp590-140-24sp-bvanwo.apps.unc.edu/auth/as/amy/888888888
A2,Giovanna Chen,Michelle Nguyen,Nadine Hughes, , ,XL News Feed / Announcements,https://youtu.be/826CZNE6djI,https://csxl-team-a2-comp590-24s.apps.unc.edu/news
A3,Lalitha Vadrevu,Pallavi Sastry,Advika Ganesh,Erin Ma, ,Student Organization Memberships / Members-only Features,https://youtu.be/wJDfkW_sXgM?si=0JRxgRlifP7SWLCr,https://csxl-team-a3-comp590-24s.apps.unc.edu/
A4,Prithvi Adiga,Trinh Kieu,Maria Thomas,Maddie Dai, ,XL News Feed / Announcements,https://youtu.be/c3ZwTti0kp0,https://csxl-team-a4-comp590-24s.apps.cloudapps.unc.edu/news
A5,Shaina Patel,Daisy Azagba,Sherly Lin,Alicia Bao, ,XL Digital Display System,https://youtu.be/6j08ktdk5eY,https://final-team-a5-comp590-140-24sp-sherly1.apps.unc.edu
A6,Asim Raja,Alexandra Marum,William Chesser,Aristotle Bernard, ,Other: Course Planner,https://youtu.be/m3JZOwOt21k,https://final-team-a6-comp590-140-24sp-bchesser.apps.unc.edu/academics/planner
A7,Jake Rogers,Saishreeya Kantamsetty,Ellie Kim,Upasana Lamsal, ,Interactive Seating Chart / Map Widget,https://youtu.be/apgRX7fywMc,https://final-team-a7-comp590-140-24sp-cellie.apps.unc.edu/
A9,Jack Huo,Jack Geng,Arnav Thakar,Jeff Zhuo, ,Interactive Seating Chart / Map Widget,https://youtu.be/NaVdG8Nnnvs,https://csxl-team-a9-comp590-24s.apps.unc.edu
B1,Ishmael Percy,Alphonzo Dixon Iii,Jayson Mbugua,Embrey Morton, ,XL News Feed / Announcements,https://youtu.be/_eoMg1URLKY,https://csxl-team-b1-comp590-140-24sp-embreezy.apps.unc.edu/
B2,Gaines Diseker,Evan Flynn,Chris Odondi,Heri Ongechi, ,Student Organization Memberships / Members-only Features,https://youtu.be/-HsEyvy73pY,https://csxl-team-b2-comp590-24s.apps.unc.edu/profile
B4,Aryan Choudhary,Thomas Carriero,Lucas Jorgensen,Madelyn Drummonds, ,XL News Feed / Announcements,https://www.youtube.com/watch?v=ABvNvN3q-0U,https://csxl-team-b4-comp590-24s.apps.unc.edu/profile/edit
B5,Noah Weaver,Ethan Crook,Jahnavi Kumar, , ,Other: Personal Showcase,https://www.youtube.com/watch?v=5HTkijZrJAc,https://csxl-team-b5-comp590-24s.apps.unc.edu
B6,Ryan Bowers,Arul Gundam,Nathan Kelete,Sanyukta Lamsal, ,XL News Feed / Announcements,https://www.youtube.com/watch?v=5TGjfkX4d00&ab_channel=ArulGundam,https://csxl-team-b6-comp590-24s.apps.unc.edu/news
B7,Caitlyn Kim,Harin Lim,Hong Liu, , ,Interactive Seating Chart / Map Widget,https://www.youtube.com/watch?v=WDWRKJ05rIQ,https://csxl-team-b7-comp590-24s.apps.unc.edu/coworking
B8,Yawen Deng,Ying Hu,,,,XL News Feed / Announcements,https://youtu.be/X2txUI2gSEI,https://csxl-team-b8-comp590-24s.apps.unc.edu
B9,Mustafa Aljumayli,Hope Fauble,Chloe Gee,Matthew Loynes, ,XL News Feed / Announcements,https://youtu.be/hviVCYsW510,https://csxl-team-b9-comp590-24s.apps.unc.edu/newsfeed
C1,Niyaz Shakeel,Raheq Hassan,Ayah Abdul-Haqq,Mostafa Edris, ,Student Organization Memberships / Members-only Features,https://www.youtube.com/watch?v=lGyR1AgyR-U,https://csxl-team-c1-comp590-24s.apps.cloudapps.unc.edu/
C2,Wisdom Okwen,Austin Campbell,Evan Murray,Scott Hoover, ,XL News Feed / Announcements,https://youtu.be/sozO9m0PrXg?si=12dFCFtndr59wMSa,https://final-team-c2-comp590-140-24sp-evanesce.apps.unc.edu/announcements
C3,Indira Van Kanegan,Olivia Xiao,Maya Mcpartland,Niah O'Briant, ,XL News Feed / Announcements,https://youtu.be/hg7IAqQ7Y2I ,https://csxl-team-c3-comp590-24s.apps.unc.edu/news 
C4,Venkata Mantri,Aaron Wang,Sujay Bhilegaonkar,Sam Bisaria, ,XL News Feed / Announcements,https://www.youtube.com/watch?v=sOkgRWpttkg,https://csxl-team-c4-comp590-24s.apps.unc.edu/
C5,Michael Diaz,Calvin Courbois,Miles Murphy,Justin Rivera, ,XL News Feed / Announcements,https://youtu.be/wA_bOIabJR8,https://csxl-team-c5-comp590-24s.apps.unc.edu/
C6,Gregory Glasby Iii,Luis Villa Jr,Connor Vines,Adrian Lanier, ,Student Organization Memberships / Members-only Features,https://www.youtube.com/watch?v=zPVB2ZGEAJQ&ab_channel=TraceGlasby,https://csxl-team-c6-comp590-24s.apps.unc.edu
C7,Manav Katarey,Joshua Grosser,Saman Sahebi,Jake Mareno, ,Student Organization Memberships / Members-only Features,https://youtu.be/oj_RawH4tm4,https://csxl-team-c7-comp590-24s.apps.unc.edu
C9,Isaac Tran,Justin Guo,Aaron Zhao,Brian Pov, ,XL News Feed / Announcements,https://youtu.be/ywE9wOJeq1E,https://test-comp590-140-24sp-aaroz.apps.unc.edu/
D1,Bodhi Harmony,Jason Manning,Cole Whaley,Danny Wang, ,Interactive Seating Chart / Map Widget,https://youtu.be/Cnw_bpsJrlk,https://csxl-team-d1-comp590-24s.apps.unc.edu
D2,Thomas Voglesonger,Wei Jiang,Ivan Wu,Benjamin Zhang, ,Interactive Seating Chart / Map Widget,https://youtu.be/9qCM0vRHXFw,https://csxl-team-d2-comp590-24s.apps.unc.edu
D3,Ahmad Raiyan,Nawfal Mohamed,Zaid Kamdar,Denizhan Kilic, ,XL News Feed / Announcements,https://youtu.be/a5n45blgjFA,https://csxl-team-d3-comp590-24s.apps.unc.edu/announcement
D4,Nicholas Sanaie,Tyler Roth,Tanner Macpherson,Mark Maio Jr, ,XL News Feed / Announcements,https://www.youtube.com/watch?v=1TSD6CjXgcg,https://csxl-team-d4-comp590-24s.apps.unc.edu/
D5,Jeremy Wang,Abhinav Mayreddy,Jeffrey Zhang,Samyuktha Vipin, ,XL News Feed / Announcements,https://youtu.be/C7IIIdFiRtQ,https://final-d5-comp590-140-24sp-zhangja.apps.unc.edu
D6,Xiaolong Huang,Chinmay Avsarkar,Luis Fajardo Jr,Kalen Byrd, ,XL News Feed / Announcements,https://youtu.be/lwIth0VWjL8,https://final-team-d6-comp590-140-24sp-kalen.apps.unc.edu/auth/as/rhona/999999999
D7,Vincent Li,Yuzhe Liu,Sarang Myoung,Diamoah Ngwayah Jr,Girish Rengadurai,XL News Feed / Announcements,https://www.youtube.com/watch?v=2Ox8uJyA1a8,https://csxl-team-d7-comp590-24s.apps.unc.edu
D9,Rishi Ranabothu,Prajwal Moharana,Jayden Lim,Swagat Adhikary, ,Other: Course Planner,https://youtu.be/Tw9g_4Nc_28,https://csxl-team-d9-comp590-24s.apps.unc.edu/about
E1,Norah Binny,Chasity Davis,Evan Menendez,Brian Britt, ,Student Organization Memberships / Members-only Features,https://youtu.be/lwa97dDYZtg?si=SmFAdI-_1m3uFVB6,https://csxl-team-e1-comp590-24s.apps.unc.edu
E2,Aryaman Sonkiya,Naveen Prabhu,Aum Kendapadi,Samanyu Dixit, ,Interactive Seating Chart / Map Widget,https://youtu.be/Kfa5kfnc-GA,https://csxl-team-e2-comp590-24s.apps.unc.edu/
E3,Thomas Kung,Leon Tran,Ryan Nguyen, , ,XL News Feed / Announcements,https://youtu.be/axR-XDQcCI4,https://csxl-team-e3-comp590-24s.apps.unc.edu/
E4,Logan Richter,Benjamin Sears,Sean Murphy Jr,Brandon Lozano, ,XL News Feed / Announcements,https://youtu.be/9j0I7uCu7Lk,https://final-team-e4-comp590-140-24sp-sirlogan.apps.unc.edu/news
E5,Armaan Punj,Thomas Smith,Raymond Zou,Harry Hong, ,Student Organization Memberships / Members-only Features,https://youtu.be/K8ekY9EvCv4,https://csxl-team-e5-comp590-140-24sp-tss.apps.unc.edu/about
E6,Jinjing Tan,Andre Rosado,,, ,XL News Feed / Announcements,https://youtu.be/msfCG1e99TI,https://csxl-team-e6a-comp590-24s.apps.unc.edu/
E7,Bennett Mangum,Emmalyn Foster,Hunter Hamrick,Albert He, ,Student Organization Memberships / Members-only Features,https://youtu.be/bEkhTi3po0c,https://csxl-team-e7-comp590-24s.apps.unc.edu/
E9,Connor Goodwin,Samuel Gilmore,Caden Alford, , ,XL Digital Display System,https://www.youtube.com/watch?v=qv16jUALlV0,https://csxl-team-e9-comp590-24s.apps.unc.edu/coworking
F1,Emilee Liggins,Jeremy Chen,Rohan Kumar, , ,XL Digital Display System,https://youtu.be/bxhsJFAgZKE,
F2,Anish Kompella,Aditya Krishna,Robert Wittmann, , ,XL News Feed / Announcements,https://youtu.be/IMLeyqRDl3A,https://csxl-team-f2-comp590-140-24sp-adi3kris.apps.unc.edu/homepage
F3,Jake Terrill,Lukas Dendrolivanos,Eric Le,David Ezeude, ,XL News Feed / Announcements,https://youtu.be/ZFjLiHgJ2Zw,https://final-team-f3-comp590-140-24sp-ericle.apps.unc.edu/newsfeed
F4,Daniel Naranjo,Vihit Nanduri,Harshith Manepalli,Alexander Machalicky, ,XL News Feed / Announcements,https://youtu.be/pX89__edJwU,https://csxl-team-f4-comp590-24s.apps.unc.edu"""

projects: list[ShowcaseProject] = []

# Parse the data.
for line in DATA.split("\n"):
    items = line.split(",")
    print(items)
    team_name = items[0]
    type = items[-3]
    video = items[-2]
    deployment = items[-1]
    team_members = [member for member in items[1:-3] if member != " "]

    new_project = ShowcaseProject(
        team_name=team_name,
        type=type,
        members=team_members,
        video_url=video,
        deployment_url=deployment,
    )

    projects.append(new_project)
