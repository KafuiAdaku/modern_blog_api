from typing import Any, List


class BlogTimeEngine:
    def __init__(self, blog: Any) -> None:
        """Initializes the blog time engine"""
        self.blog = blog

        self.words_per_minute = 250

        self.banner_image_adjustment_time = round(1 / 6, 3)

    def check_blog_has_banner_image(self) -> bool:
        """Check if blog has a banner image"""
        has_banner_image = True
        if not self.blog.banner_image:
            has_banner_image = False
            self.banner_image_adjustment_time = 0
        return has_banner_image

    def get_title(self) -> str:
        """Get the title of the blog"""
        return self.blog.title

    def get_tags(self) -> List[str]:
        """Get the tags of the blog"""
        tag_words = []
        [tag_words.extend(tag_word.split()) for
            tag_word in self.blog.list_of_tags]
        return tag_words

    def get_body(self) -> str:
        """Get the body of the blog"""
        return self.blog.body

    def get_description(self) -> str:
        """Get the description of the blog"""
        return self.blog.description

    def get_blog_details(self) -> List[str]:
        """Get the details of the blog"""
        details = []
        details.extend(self.get_title().split())
        details.extend(self.get_body().split())
        details.extend(self.get_description().split())
        details.extend(self.get_tags())
        return details

    def get_read_time(self) -> str:
        """Get the read time of the blog"""
        word_length = len(self.get_blog_details())
        read_time = 0
        self.check_blog_has_banner_image()

        if word_length:
            time_to_read = word_length / self.words_per_minute
            if time_to_read < 1:
                read_time = (
                    str(round((time_to_read +
                        self.banner_image_adjustment_time) * 60))
                    + " second(s)"
                )
            else:
                read_time = (
                    str(round(time_to_read +
                        self.banner_image_adjustment_time))
                    + " minute(s)"
                )
            return read_time
