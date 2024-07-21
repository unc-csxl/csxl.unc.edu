"""Contains mock data for the live demo of the article feature."""

import pytest
from sqlalchemy.orm import Session
from ....models.articles import *
from ....entities.article_entity import ArticleEntity, article_author_table
from datetime import datetime

from ..reset_table_id_seq import reset_table_id_seq

from .. import user_data

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

# Sample Articles

announcement = ArticleDraft(
    id=0,
    slug="my-announcement",
    state=ArticleState.PUBLISHED,
    title="Sample Announcement",
    image_url="https://i.etsystatic.com/22085368/r/il/716804/2576209117/il_570xN.2576209117_ran0.jpg",
    synopsis="The CSXL Web Application is undergoing a major update this summer, including adding new features, improving the site's performance, and undergoing a major redesign to reflect the modern design standards.",
    body="""Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do *eiusmod tempor* incididunt ut labore et dolore magna aliqua. Dui nunc mattis enim ut. At volutpat diam ut venenatis tellus in metus vulputate. Malesuada fames ac turpis egestas integer eget aliquet. Lorem ipsum dolor sit amet consectetur adipiscing elit ut. Eget felis eget nunc lobortis mattis aliquam faucibus purus. Arcu cursus vitae congue mauris rhoncus aenean vel elit scelerisque. Nisi vitae suscipit tellus mauris a diam maecenas. Sem et tortor consequat id porta nibh. Sagittis purus sit amet volutpat. Massa eget egestas purus viverra accumsan in nisl nisi. Platea dictumst quisque sagittis purus sit amet volutpat.

Sit amet consectetur adipiscing elit duis tristique sollicitudin nibh sit. Velit sed ullamcorper morbi tincidunt ornare massa. Bibendum ut tristique et egestas quis ipsum. Neque vitae tempus quam pellentesque nec nam aliquam sem. Scelerisque viverra mauris in aliquam sem fringilla ut morbi. Lectus proin nibh nisl condimentum. Viverra nibh cras pulvinar mattis nunc sed blandit libero volutpat. Non diam phasellus vestibulum lorem sed risus. Urna nunc id cursus metus aliquam eleifend mi. Orci a scelerisque purus semper. Non nisi est sit amet facilisis magna etiam. Sed libero enim sed faucibus. Facilisi cras fermentum odio eu feugiat pretium nibh ipsum. Velit ut tortor pretium viverra suspendisse potenti nullam ac tortor. Condimentum lacinia quis vel eros donec ac. Diam sollicitudin tempor id eu nisl nunc mi ipsum. Vehicula ipsum a arcu cursus vitae congue mauris. Neque viverra justo nec ultrices dui sapien eget mi proin. Blandit libero volutpat sed cras ornare. Imperdiet massa tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada.

Bibendum ut tristique et egestas. Ullamcorper a lacus vestibulum sed arcu non odio euismod. Pretium nibh ipsum consequat nisl vel pretium lectus. Viverra accumsan in nisl nisi. Tristique nulla aliquet enim tortor at auctor urna nunc id. Integer eget aliquet nibh praesent tristique. In eu mi bibendum neque egestas congue quisque. Urna condimentum mattis pellentesque id nibh. Dignissim cras tincidunt lobortis feugiat. Non consectetur a erat nam at lectus urna duis. A condimentum vitae sapien pellentesque habitant morbi tristique senectus et. Tortor dignissim convallis aenean et tortor at risus viverra. Vitae nunc sed velit dignissim sodales ut eu sem integer. Pretium vulputate sapien nec sagittis aliquam malesuada bibendum. Sit amet consectetur adipiscing elit pellentesque habitant morbi tristique. Enim ut tellus elementum sagittis vitae et leo. A scelerisque purus semper eget duis at.

Tempus imperdiet nulla malesuada pellentesque. Vulputate odio ut enim blandit volutpat. Integer eget aliquet nibh praesent tristique magna sit. Habitant morbi tristique senectus et netus et. Auctor elit sed vulputate mi sit amet. Scelerisque varius morbi enim nunc. Arcu felis bibendum ut tristique et egestas. Vulputate mi sit amet mauris commodo quis. Amet consectetur adipiscing elit ut aliquam purus. Viverra maecenas accumsan lacus vel facilisis volutpat.

Viverra nibh cras pulvinar mattis nunc sed blandit libero volutpat. Tincidunt dui ut ornare lectus sit. Morbi leo urna molestie at. A diam maecenas sed enim ut sem viverra aliquet eget. In tellus integer feugiat scelerisque varius morbi enim nunc faucibus. In iaculis nunc sed augue lacus viverra vitae. Vitae semper quis lectus nulla at volutpat diam. Quis blandit turpis cursus in hac habitasse platea. Est lorem ipsum dolor sit amet consectetur adipiscing elit. Turpis egestas maecenas pharetra convallis posuere morbi leo. Dictumst vestibulum rhoncus est pellentesque.""",
    published=datetime.now(),
    last_modified=datetime.now(),
    is_announcement=True,
    organization_id=None,
    authors=[],
)

article_one = ArticleDraft(
    id=1,
    slug="article-one",
    state=ArticleState.PUBLISHED,
    title="Article One",
    image_url="https://i.etsystatic.com/22085368/r/il/716804/2576209117/il_570xN.2576209117_ran0.jpg",
    synopsis="Today marks a momentous day in the CSXL’s history - our brand new website has launched with an all-new design and new features to kick-start your 2024-2025 academic year as a CS major!",
    body="""Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do *eiusmod tempor* incididunt ut labore et dolore magna aliqua. Dui nunc mattis enim ut. At volutpat diam ut venenatis tellus in metus vulputate. Malesuada fames ac turpis egestas integer eget aliquet. Lorem ipsum dolor sit amet consectetur adipiscing elit ut. Eget felis eget nunc lobortis mattis aliquam faucibus purus. Arcu cursus vitae congue mauris rhoncus aenean vel elit scelerisque. Nisi vitae suscipit tellus mauris a diam maecenas. Sem et tortor consequat id porta nibh. Sagittis purus sit amet volutpat. Massa eget egestas purus viverra accumsan in nisl nisi. Platea dictumst quisque sagittis purus sit amet volutpat.
## Example Subeading
Sit amet consectetur adipiscing elit duis tristique sollicitudin nibh sit. Velit sed ullamcorper morbi tincidunt ornare massa. Bibendum ut tristique et egestas quis ipsum. Neque vitae tempus quam pellentesque nec nam aliquam sem. Scelerisque viverra mauris in aliquam sem fringilla ut morbi. Lectus proin nibh nisl condimentum. Viverra nibh cras pulvinar mattis nunc sed blandit libero volutpat. Non diam phasellus vestibulum lorem sed risus. Urna nunc id cursus metus aliquam eleifend mi. Orci a scelerisque purus semper. Non nisi est sit amet facilisis magna etiam. Sed libero enim sed faucibus. Facilisi cras fermentum odio eu feugiat pretium nibh ipsum. Velit ut tortor pretium viverra suspendisse potenti nullam ac tortor. Condimentum lacinia quis vel eros donec ac. Diam sollicitudin tempor id eu nisl nunc mi ipsum. Vehicula ipsum a arcu cursus vitae congue mauris. Neque viverra justo nec ultrices dui sapien eget mi proin. Blandit libero volutpat sed cras ornare. Imperdiet massa tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada.
## Example Subeading
Bibendum ut tristique et egestas. Ullamcorper a lacus vestibulum sed arcu non odio euismod. Pretium nibh ipsum consequat nisl vel pretium lectus. Viverra accumsan in nisl nisi. Tristique nulla aliquet enim tortor at auctor urna nunc id. Integer eget aliquet nibh praesent tristique. In eu mi bibendum neque egestas congue quisque. Urna condimentum mattis pellentesque id nibh. Dignissim cras tincidunt lobortis feugiat. Non consectetur a erat nam at lectus urna duis. A condimentum vitae sapien pellentesque habitant morbi tristique senectus et. Tortor dignissim convallis aenean et tortor at risus viverra. Vitae nunc sed velit dignissim sodales ut eu sem integer. Pretium vulputate sapien nec sagittis aliquam malesuada bibendum. Sit amet consectetur adipiscing elit pellentesque habitant morbi tristique. Enim ut tellus elementum sagittis vitae et leo. A scelerisque purus semper eget duis at.
## Example Subeading
Tempus imperdiet nulla malesuada pellentesque. Vulputate odio ut enim blandit volutpat. Integer eget aliquet nibh praesent tristique magna sit. Habitant morbi tristique senectus et netus et. Auctor elit sed vulputate mi sit amet. Scelerisque varius morbi enim nunc. Arcu felis bibendum ut tristique et egestas. Vulputate mi sit amet mauris commodo quis. Amet consectetur adipiscing elit ut aliquam purus. Viverra maecenas accumsan lacus vel facilisis volutpat.
## Example Subeading
Viverra nibh cras pulvinar mattis nunc sed blandit libero volutpat. Tincidunt dui ut ornare lectus sit. Morbi leo urna molestie at. A diam maecenas sed enim ut sem viverra aliquet eget. In tellus integer feugiat scelerisque varius morbi enim nunc faucibus. In iaculis nunc sed augue lacus viverra vitae. Vitae semper quis lectus nulla at volutpat diam. Quis blandit turpis cursus in hac habitasse platea. Est lorem ipsum dolor sit amet consectetur adipiscing elit. Turpis egestas maecenas pharetra convallis posuere morbi leo. Dictumst vestibulum rhoncus est pellentesque.""",
    published=datetime.now(),
    last_modified=datetime.now(),
    is_announcement=False,
    organization_id=None,
    authors=[],
)

article_two = ArticleDraft(
    id=2,
    slug="article-two",
    state=ArticleState.PUBLISHED,
    title="Article Two",
    image_url="https://i.etsystatic.com/22085368/r/il/716804/2576209117/il_570xN.2576209117_ran0.jpg",
    synopsis="I began to notice these mysterious, noisy rubber ducks appear around the CSXL. Soon, they entered by backpack, car, and shoes! Who keeps leaving these around? CSXL journalist Noah Smith investigates.",
    body="""Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do *eiusmod tempor* incididunt ut labore et dolore magna aliqua. Dui nunc mattis enim ut. At volutpat diam ut venenatis tellus in metus vulputate. Malesuada fames ac turpis egestas integer eget aliquet. Lorem ipsum dolor sit amet consectetur adipiscing elit ut. Eget felis eget nunc lobortis mattis aliquam faucibus purus. Arcu cursus vitae congue mauris rhoncus aenean vel elit scelerisque. Nisi vitae suscipit tellus mauris a diam maecenas. Sem et tortor consequat id porta nibh. Sagittis purus sit amet volutpat. Massa eget egestas purus viverra accumsan in nisl nisi. Platea dictumst quisque sagittis purus sit amet volutpat.

Sit amet consectetur adipiscing elit duis tristique sollicitudin nibh sit. Velit sed ullamcorper morbi tincidunt ornare massa. Bibendum ut tristique et egestas quis ipsum. Neque vitae tempus quam pellentesque nec nam aliquam sem. Scelerisque viverra mauris in aliquam sem fringilla ut morbi. Lectus proin nibh nisl condimentum. Viverra nibh cras pulvinar mattis nunc sed blandit libero volutpat. Non diam phasellus vestibulum lorem sed risus. Urna nunc id cursus metus aliquam eleifend mi. Orci a scelerisque purus semper. Non nisi est sit amet facilisis magna etiam. Sed libero enim sed faucibus. Facilisi cras fermentum odio eu feugiat pretium nibh ipsum. Velit ut tortor pretium viverra suspendisse potenti nullam ac tortor. Condimentum lacinia quis vel eros donec ac. Diam sollicitudin tempor id eu nisl nunc mi ipsum. Vehicula ipsum a arcu cursus vitae congue mauris. Neque viverra justo nec ultrices dui sapien eget mi proin. Blandit libero volutpat sed cras ornare. Imperdiet massa tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada.

Bibendum ut tristique et egestas. Ullamcorper a lacus vestibulum sed arcu non odio euismod. Pretium nibh ipsum consequat nisl vel pretium lectus. Viverra accumsan in nisl nisi. Tristique nulla aliquet enim tortor at auctor urna nunc id. Integer eget aliquet nibh praesent tristique. In eu mi bibendum neque egestas congue quisque. Urna condimentum mattis pellentesque id nibh. Dignissim cras tincidunt lobortis feugiat. Non consectetur a erat nam at lectus urna duis. A condimentum vitae sapien pellentesque habitant morbi tristique senectus et. Tortor dignissim convallis aenean et tortor at risus viverra. Vitae nunc sed velit dignissim sodales ut eu sem integer. Pretium vulputate sapien nec sagittis aliquam malesuada bibendum. Sit amet consectetur adipiscing elit pellentesque habitant morbi tristique. Enim ut tellus elementum sagittis vitae et leo. A scelerisque purus semper eget duis at.

Tempus imperdiet nulla malesuada pellentesque. Vulputate odio ut enim blandit volutpat. Integer eget aliquet nibh praesent tristique magna sit. Habitant morbi tristique senectus et netus et. Auctor elit sed vulputate mi sit amet. Scelerisque varius morbi enim nunc. Arcu felis bibendum ut tristique et egestas. Vulputate mi sit amet mauris commodo quis. Amet consectetur adipiscing elit ut aliquam purus. Viverra maecenas accumsan lacus vel facilisis volutpat.

Viverra nibh cras pulvinar mattis nunc sed blandit libero volutpat. Tincidunt dui ut ornare lectus sit. Morbi leo urna molestie at. A diam maecenas sed enim ut sem viverra aliquet eget. In tellus integer feugiat scelerisque varius morbi enim nunc faucibus. In iaculis nunc sed augue lacus viverra vitae. Vitae semper quis lectus nulla at volutpat diam. Quis blandit turpis cursus in hac habitasse platea. Est lorem ipsum dolor sit amet consectetur adipiscing elit. Turpis egestas maecenas pharetra convallis posuere morbi leo. Dictumst vestibulum rhoncus est pellentesque.""",
    published=datetime.now(),
    last_modified=datetime.now(),
    is_announcement=False,
    organization_id=None,
    authors=[],
)

new_article = ArticleDraft(
    id=3,
    slug="article-three",
    state=ArticleState.PUBLISHED,
    title="Article Three",
    image_url="https://i.etsystatic.com/22085368/r/il/716804/2576209117/il_570xN.2576209117_ran0.jpg",
    synopsis="I began to notice these mysterious, noisy rubber ducks appear around the CSXL. Soon, they entered by backpack, car, and shoes! Who keeps leaving these around? CSXL journalist Noah Smith investigates.",
    body="""Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do *eiusmod tempor* incididunt ut labore et dolore magna aliqua. Dui nunc mattis enim ut. At volutpat diam ut venenatis tellus in metus vulputate. Malesuada fames ac turpis egestas integer eget aliquet. Lorem ipsum dolor sit amet consectetur adipiscing elit ut. Eget felis eget nunc lobortis mattis aliquam faucibus purus. Arcu cursus vitae congue mauris rhoncus aenean vel elit scelerisque. Nisi vitae suscipit tellus mauris a diam maecenas. Sem et tortor consequat id porta nibh. Sagittis purus sit amet volutpat. Massa eget egestas purus viverra accumsan in nisl nisi. Platea dictumst quisque sagittis purus sit amet volutpat.

Sit amet consectetur adipiscing elit duis tristique sollicitudin nibh sit. Velit sed ullamcorper morbi tincidunt ornare massa. Bibendum ut tristique et egestas quis ipsum. Neque vitae tempus quam pellentesque nec nam aliquam sem. Scelerisque viverra mauris in aliquam sem fringilla ut morbi. Lectus proin nibh nisl condimentum. Viverra nibh cras pulvinar mattis nunc sed blandit libero volutpat. Non diam phasellus vestibulum lorem sed risus. Urna nunc id cursus metus aliquam eleifend mi. Orci a scelerisque purus semper. Non nisi est sit amet facilisis magna etiam. Sed libero enim sed faucibus. Facilisi cras fermentum odio eu feugiat pretium nibh ipsum. Velit ut tortor pretium viverra suspendisse potenti nullam ac tortor. Condimentum lacinia quis vel eros donec ac. Diam sollicitudin tempor id eu nisl nunc mi ipsum. Vehicula ipsum a arcu cursus vitae congue mauris. Neque viverra justo nec ultrices dui sapien eget mi proin. Blandit libero volutpat sed cras ornare. Imperdiet massa tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada.

Bibendum ut tristique et egestas. Ullamcorper a lacus vestibulum sed arcu non odio euismod. Pretium nibh ipsum consequat nisl vel pretium lectus. Viverra accumsan in nisl nisi. Tristique nulla aliquet enim tortor at auctor urna nunc id. Integer eget aliquet nibh praesent tristique. In eu mi bibendum neque egestas congue quisque. Urna condimentum mattis pellentesque id nibh. Dignissim cras tincidunt lobortis feugiat. Non consectetur a erat nam at lectus urna duis. A condimentum vitae sapien pellentesque habitant morbi tristique senectus et. Tortor dignissim convallis aenean et tortor at risus viverra. Vitae nunc sed velit dignissim sodales ut eu sem integer. Pretium vulputate sapien nec sagittis aliquam malesuada bibendum. Sit amet consectetur adipiscing elit pellentesque habitant morbi tristique. Enim ut tellus elementum sagittis vitae et leo. A scelerisque purus semper eget duis at.

Tempus imperdiet nulla malesuada pellentesque. Vulputate odio ut enim blandit volutpat. Integer eget aliquet nibh praesent tristique magna sit. Habitant morbi tristique senectus et netus et. Auctor elit sed vulputate mi sit amet. Scelerisque varius morbi enim nunc. Arcu felis bibendum ut tristique et egestas. Vulputate mi sit amet mauris commodo quis. Amet consectetur adipiscing elit ut aliquam purus. Viverra maecenas accumsan lacus vel facilisis volutpat.

Viverra nibh cras pulvinar mattis nunc sed blandit libero volutpat. Tincidunt dui ut ornare lectus sit. Morbi leo urna molestie at. A diam maecenas sed enim ut sem viverra aliquet eget. In tellus integer feugiat scelerisque varius morbi enim nunc faucibus. In iaculis nunc sed augue lacus viverra vitae. Vitae semper quis lectus nulla at volutpat diam. Quis blandit turpis cursus in hac habitasse platea. Est lorem ipsum dolor sit amet consectetur adipiscing elit. Turpis egestas maecenas pharetra convallis posuere morbi leo. Dictumst vestibulum rhoncus est pellentesque.""",
    published=datetime.now(),
    last_modified=datetime.now(),
    is_announcement=False,
    organization_id=None,
    authors=[],
)

articles = [announcement, article_one, article_two]
articles_no_announcement = [article_one, article_two]

author_associations = [
    (announcement, user_data.root),
    (article_one, user_data.root),
    (article_two, user_data.root),
]


def insert_fake_data(session: Session):

    # Step 1: Add articles to database
    for article in articles:
        entity = ArticleEntity.from_draft(article)
        session.add(entity)

    reset_table_id_seq(
        session,
        ArticleEntity,
        ArticleEntity.id,
        len(articles) + 1,
    )

    session.commit()

    # Step 2: Add authors to the datbase

    for article, author in author_associations:
        session.execute(
            article_author_table.insert().values(
                {"user_id": author.id, "article_id": article.id}
            )
        )
        session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
