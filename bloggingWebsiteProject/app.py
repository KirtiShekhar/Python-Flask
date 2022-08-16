from flask import Flask,request,redirect
from flask import render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BlogPost.db'
sqliteDatabase = SQLAlchemy(app)


class BlogPost(sqliteDatabase.Model):
    blogPostId = sqliteDatabase.Column(sqliteDatabase.Integer, primary_key=True, nullable=False)
    blogPostContent = sqliteDatabase.Column(sqliteDatabase.Text, nullable=False)
    blogPostAuthor = sqliteDatabase.Column(sqliteDatabase.Text, nullable=False, default=str(datetime.utcnow))
    blogPostPublished = sqliteDatabase.Column(sqliteDatabase.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "Blogs Saved Details:" + "\n" + "blogPostId : " + str(
            self.blogPostId) + "\n" + "blogPostContent : " + self.blogPostContent + "\n" + "blogPostAuthor : " + \
               self.blogPostAuthor + "\n" + "blogPostPublished : " + str(self.blogPostPublished)

@app.route('/blogPost/post/get', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        postBlogPostContent = request.form['blogPostContent']
        postBlogPostAuthor = request.form['blogPostAuthor']
        sqliteDatabase.session.add(BlogPost(blogPostContent=postBlogPostContent,blogPostAuthor=postBlogPostAuthor))
        sqliteDatabase.session.commit()
        return redirect('/blogPost/post/get')
    else:
        BlogPosts = BlogPost.query.all()
        return render_template('blogPostHome.html',BlogPosts=BlogPosts)


@app.route('/about')
def about():
    return render_template('blogPostAbout.html')

@app.route('/delete/<int:blogPostId>/')
def delete(blogPostId):
    postBlogPostDelete = BlogPost.query.get_or_404(blogPostId)
    sqliteDatabase.session.delete(postBlogPostDelete)
    sqliteDatabase.session.commit()
    return redirect('/blogPost/post/get')

@app.route('/edit/<int:blogPostId>/', methods=['GET', 'POST'])
def editBlogPost(blogPostId):
    postBlogPostEdit = BlogPost.query.get_or_404(blogPostId)
    if request.method == 'POST':
        postBlogPostEdit.editBlogPostContent = request.form['blogPostContent']
        postBlogPostEdit.editBlogPostAuthor = request.form['blogPostAuthor']
        sqliteDatabase.session.commit()
        return redirect('/blogPost/post/get')
    else:
        return render_template('blogPostEdit.html',postBlogPostEdit=postBlogPostEdit)

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == "__main__":
    app.run(debug=True)
