import pytest

from sqlalchemy.orm import Session
from ....models.showcase_project import *

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

# Do not try this at home.

DATA = """A1,Deysi Morales-Magadan,Luis Rivera Gonzalez,Bailey Van Wormer, , ,XL News Feed / Announcements
A2,Giovanna Chen,Michelle Nguyen,Nadine Hughes, , ,XL News Feed / Announcements
A3,Lalitha Vadrevu,Pallavi Sastry,Advika Ganesh,Erin Ma, ,Student Organization Memberships / Members-only Features
A4,Prithvi Adiga,Trinh Kieu,Maria Thomas,Maddie Dai, ,XL News Feed / Announcements
A5,Shaina Patel,Daisy Azagba,Sherly Lin,Alicia Bao, ,XL Digital Display System
A6,Asim Raja,Alexandra Marum,William Chesser,Aristotle Bernard, ,XL Digital Display System
A7,Jake Rogers,Saishreeya Kantamsetty,Ellie Kim,Upasana Lamsal, ,Interactive Seating Chart / Map Widget
A9,Jack Huo,Jack Geng,Arnav Thakar,Jeff Zhuo, ,Interactive Seating Chart / Map Widget
B1,Ishmael Percy,Alphonzo Dixon Iii,Jayson Mbugua,Embrey Morton, ,XL News Feed / Announcements
B2,Gaines Diseker,Evan Flynn,Chris Odondi,Heri Ongechi, ,Student Organization Memberships / Members-only Features
B4,Aryan Choudhary,Thomas Carriero,Lucas Jorgensen,Madelyn Drummonds, ,XL News Feed / Announcements
B5,Noah Weaver,Ethan Crook,Jahnavi Kumar, , ,Interactive Seating Chart / Map Widget
B6,Ryan Bowers,Arul Gundam,Nathan Kelete,Sanyukta Lamsal, ,XL News Feed / Announcements
B7,Caitlyn Kim,Harin Lim,Hong Liu, , ,Interactive Seating Chart / Map Widget
B8,Yawen Deng,Ying Hu,,,,XL News Feed / Announcements
B9,Mustafa Aljumayli,Hope Fauble,Chloe Gee,Matthew Loynes, ,XL News Feed / Announcements
C1,Niyaz Shakeel,Raheq Hassan,Ayah Abdul-Haqq,Mostafa Edris, ,Student Organization Memberships / Members-only Features
C2,Wisdom Okwen,Austin Campbell,Evan Murray,Scott Hoover, ,XL News Feed / Announcements
C3,Indira Van Kanegan,Olivia Xiao,Maya Mcpartland,Niah O'Briant, ,XL News Feed / Announcements
C4,Venkata Mantri,Aaron Wang,Sujay Bhilegaonkar,Sam Bisaria, ,XL News Feed / Announcements
C5,Michael Diaz,Calvin Courbois,Miles Murphy,Justin Rivera, ,XL News Feed / Announcements
C6,Gregory Glasby Iii,Luis Villa Jr,Connor Vines,Adrian Lanier, ,Student Organization Memberships / Members-only Features
C7,Manav Katarey,Joshua Grosser,Saman Sahebi,Jake Mareno, ,Student Organization Memberships / Members-only Features
C9,Isaac Tran,Justin Guo,Aaron Zhao,Brian Pov, ,XL News Feed / Announcements
D1,Bodhi Harmony,Jason Manning,Cole Whaley,Danny Wang, ,Interactive Seating Chart / Map Widget
D2,Thomas Voglesonger,Wei Jiang,Ivan Wu,Benjamin Zhang, ,Interactive Seating Chart / Map Widget
D3,Ahmad Raiyan,Nawfal Mohamed,Zaid Kamdar,Denizhan Kilic, ,XL News Feed / Announcements
D4,Nicholas Sanaie,Tyler Roth,Tanner Macpherson,Mark Maio Jr, ,XL News Feed / Announcements
D5,Jeremy Wang,Abhinav Mayreddy,Jeffrey Zhang,Samyuktha Vipin, ,XL News Feed / Announcements
D6,Xiaolong Huang,Chinmay Avsarkar,Luis Fajardo Jr,Kalen Byrd, ,XL News Feed / Announcements
D7,Vincent Li,Yuzhe Liu,Sarang Myoung,Diamoah Ngwayah Jr,Girish Rengadurai,XL News Feed / Announcements
D9,Rishi Ranabothu,Prajwal Moharana,Jayden Lim,Swagat Adhikary, ,Interactive Seating Chart / Map Widget
E1,Norah Binny,Chasity Davis,Evan Menendez,Brian Britt, ,Student Organization Memberships / Members-only Features
E2,Aryaman Sonkiya,Naveen Prabhu,Aum Kendapadi,Samanyu Dixit, ,Interactive Seating Chart / Map Widget
E3,Thomas Kung,Leon Tran,Ryan Nguyen, , ,XL News Feed / Announcements
E4,Logan Richter,Benjamin Sears,Sean Murphy Jr,Brandon Lozano, ,XL News Feed / Announcements
E5,Armaan Punj,Thomas Smith,Raymond Zou,Harry Hong, ,Student Organization Memberships / Members-only Features
E5,Armaan Punj,Harry Hong,Thomas Smith,Raymond Zou, ,Student Organization Memberships / Members-only Features
E6,Jinjing Tan,Andre Rosado,,, ,XL News Feed / Announcements
E7,Bennett Mangum,Emmalyn Foster,Hunter Hamrick,Albert He, ,Student Organization Memberships / Members-only Features
E9,Connor Goodwin,Samuel Gilmore,Caden Alford, , ,XL Digital Display System
F1,Emilee Liggins,Jeremy Chen,Rohan Kumar, , ,XL Digital Display System
F2,Anish Kompella,Aditya Krishna,Robert Wittmann, , ,XL News Feed / Announcements
F3,Jake Terrill,Lukas Dendrolivanos,Eric Le,David Ezeude, ,XL News Feed / Announcements
F4,Daniel Naranjo,Vihit Nanduri,Harshith Manepalli,Alexander Machalicky, ,XL News Feed / Announcements"""

projects: list[ShowcaseProject] = []

# Parse the data.
for line in DATA.split("\n"):
    items = line.split(",")
    team_name = items[0]
    type = items[-1]
    team_members = [member for member in items[1:-1] if member != " "]

    new_project = ShowcaseProject(team_name=team_name, type=type, members=team_members)

    projects.append(new_project)
