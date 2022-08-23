from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Password reset
from .tokens import account_activation_token
# Email
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.conf import settings

from django.contrib.auth import update_session_auth_hash
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def signup(request, *args, **kwargs):

	if request.method == 'POST':
		form = UserRegistrationForm(request.POST or None)
		profile_form = ProfileForm(request.POST or None)

		if form.is_valid() and profile_form.is_valid():
			user = form.save(commit=False)
			profile = profile_form.save(commit=False)

			passwd1 = form.cleaned_data.get('password1')

			user.set_password(passwd1)
			user.save()

			profile.user = user
			profile.save()
			messages.success(request, "User successfuly registered.")

			return redirect('accounts:signin')

		else:
			print(form.errors, profile_form.errors)
	else:
		form = UserRegistrationForm()
		profile_form = ProfileForm(request.POST or None)

	context = {
		'form': form,
		'profile_form': profile_form,
	}
	return render(request, 'register_user.html', context)


def signin(request, *args, **kargs):
	if request.user.is_authenticated:
		return redirect('dashboard:index')

	if request.method == 'POST':
		form = LoginForm(request.POST or None)
		if form.is_valid():
			# Login Form
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')

			# authentication
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('dashboard:index')
			else:
				messages.error(request, "Invalid username or password.")

	else:
		form = LoginForm()

	context = {
		'form': form,
	}
	return render(request, 'login.html', context)


@login_required
def signout(request, *args, **kwargs):
	logout(request)
	return redirect('accounts:signin')


@login_required
def view_user_profile(request, *args, **kwargs):

	context = {
	}
	return render(request, 'view_user_profile.html', context)


@login_required
def edit_user_profile(request, *args, **kwargs):
	user = User.objects.filter(id=request.user.id).first()

	if request.method == 'POST':
		form = UpdateUserForm(request.POST or None, instance=user)
		profile_form = ProfileForm(request.POST or None, instance=user.profile)

		if form.is_valid() and profile_form.is_valid():
			form.save()
			profile_form.save()

			return redirect('accounts:view_user_profile')

	else:
		form = UpdateUserForm(instance=user)
		profile_form = ProfileForm(instance=user.profile)

	context = {
		'form': form,
		'profile_form': profile_form,
	}
	return render(request, 'edit_user_profile.html', context)


# Change password
@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST or None)
		if form.is_valid():
			form.save()

			return redirect('accounts:view_user_profile')

	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'change-password.html', {'form': form})


def reset_password(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		print(user, account_activation_token.check_token(user, token))
		login(request, user)
		return redirect('accounts:reset_password_form')
	else:
		return render(request, 'email/reset_password_failed.html', {'email': user.profile.email})


def reset_password_form(request, *args, **kwargs):
	user = request.user
	if request.method == "POST":
		form = SetPasswordForm(user, request.POST)
		if form.is_valid():
			new_user = form.save()
			logout(request)
			return render(request, 'email/reset_password_success.html', {'email': user.profile.email})
		else:
			print(form.errors)
	else:
		form = SetPasswordForm(user)
	context = {
		'form': form,
		'user': user,
	}
	return render(request, 'email/reset_password_form.html', context)


def reset_password_success(request, *args, **kwargs):
	email = kwargs.get('email')
	logout(request)
	return render(request, 'email/reset_password_success.html', {'email': email})


def reset_password_failed(request, *args, **kwargs):
	logout(request)
	return render(request, 'email/reset_password_failed.html', {{'email': ''}})


def reset_password_email(request):
	if request.method == "POST":

		form = ResetPassForm(request.POST)

		if form.is_valid():
			email = form.cleaned_data['email']
			print(email)

			try:
				profile = Profile.objects.filter(email=email).first()

				current_site = get_current_site(request)
				if profile:
					subject = "Password Reset"
					html_message = render_to_string("email/password_reset_email.html", {
						'fullname': '{} {}'.format(profile.first_name, profile.last_name),
						# 'user': user,
						'domain': current_site.domain,
						'uid': urlsafe_base64_encode(force_bytes(profile.user.pk)),
						'token': account_activation_token.make_token(profile.user),
					})

					message = strip_tags(html_message)
					from_email = 'SHORTNER <support@gopronow.tech>'

					recipient_list = [profile.email]

					email = EmailMultiAlternatives(
						subject, message, from_email, recipient_list)
					email.attach_alternative(html_message, "text/html")
					email.send()

					return redirect('accounts:password_reset_success', profile.email)
				else:
					messages.error(
						request, "Invalid email address, please try again.")
					return redirect('accounts:reset_password_email')

			except Exception as e:
				print(e)
				messages.error(
					request, "Error something went wrong, please try again.")
				return redirect('accounts:reset_password_email')
		else:
			print(form.errors)
	else:
		form = ResetPassForm()

	context = {
		'form': form
	}

	template_name = 'email/reset_password_email.html'

	return render(request, template_name, context)


def password_reset_success(request, *args, **kwargs):
	email = kwargs.get('email')
	return render(request, 'password_reset_success.html', {'email': email})

def resend_password_reset_email(request, *args, **kwargs):
	email = kwargs.get('email')
	try:
		profile = Profile.objects.filter(
			email=email).first()
		
		current_site = get_current_site(request)
		if profile:
			subject = "Password Reset"
			html_message = render_to_string("email/password_reset_email.html", {
                            'fullname': '{} {}'.format(profile.first_name, profile.last_name),

				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(profile.user.pk)),
				'token': account_activation_token.make_token(profile.user),
			})

			message = strip_tags(html_message)
			from_email = 'SHORTNER <support@gopronow.tech>'

			recipient_list = [profile.email]

			email = EmailMultiAlternatives(
				subject, message, from_email, recipient_list)
			email.attach_alternative(html_message, "text/html")
			email.send()
   
			response = {"success": True}
			return redirect('accounts:password_reset_success', profile.email)
		else:
			return redirect('accounts:reset_password_email')

	except Exception as e:
		print(e)
		return redirect('accounts:reset_password_email')
