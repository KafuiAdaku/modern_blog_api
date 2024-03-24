from typing import Any, List


class BlogReadTimeEngine:
    def __init__(self, blog: Any) -> None:
        """
        Initializes the BlogReadTimeEngine with the given
            blog object.

        Args:
            blog (Any): The blog object to analyze.
        """
        self.blog = blog

        self.words_per_minute = 250

        self.banner_image_adjustment_time = round(1 / 6, 3)

    def check_blog_has_banner_image(self) -> bool:
        """
        Checks if the blog has a banner image.

        Returns:
            bool: True if the blog has a banner image,
                False otherwise.
        """
        has_banner_image = True
        if not self.blog.banner_image:
            has_banner_image = False
            self.banner_image_adjustment_time = 0
        return has_banner_image

    def get_title(self) -> str:
        """
        Retrieves the title of the blog.

        Returns:
            str: The title of the blog.
        """
        return self.blog.title

    def get_tags(self) -> List[str]:
        """
        Retrieves the tags associated with the blog.

        Returns:
            List[str]: A list of tag words.
        """
        tag_words = []
        [tag_words.extend(tag_word.split()) for tag_word in self.blog.list_of_tags]
        return tag_words

    def get_body(self) -> str:
        """
        Retrieves the body content of the blog.

        Returns:
            str: The body content of the blog.
        """
        return self.blog.body

    def get_description(self) -> str:
        """
        Retrieves the description of the blog.

        Returns:
            str: The description of the blog.
        """
        return self.blog.description

    def get_blog_details(self) -> List[str]:
        """
        Retrieves various details of the blog.

        Returns:
            List[str]: A list containing the title, body,
                description, and tags of the blog.
        """
        details = []
        details.extend(self.get_title().split())
        details.extend(self.get_body().split())
        details.extend(self.get_description().split())
        details.extend(self.get_tags())
        return details

    def get_read_time(self) -> str:
        """
        Calculates the estimated read time of the blog.

        Returns:
            str: The estimated read time in minutes or seconds.
        """
        word_length = len(self.get_blog_details())
        read_time = 0
        self.check_blog_has_banner_image()

        if word_length:
            time_to_read = word_length / self.words_per_minute
            if time_to_read < 1:
                read_time = (
                    str(round((time_to_read + self.banner_image_adjustment_time) * 60))
                    + " second(s)"
                )
            else:
                read_time = (
                    str(round(time_to_read + self.banner_image_adjustment_time))
                    + " minute(s)"
                )
            return read_time
